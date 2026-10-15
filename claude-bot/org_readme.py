#!/usr/bin/env python3
"""
claude_bot: keep the org profile README's repository catalog current.

  1. Lists every repository in the org through the GitHub REST API.
  2. Keeps the category and description of repos already in the catalog.
     New repos are placed and described by Claude through the FSU Azure APIM
     gateway (one call for all of them). Without the AI they go under "Other"
     with their GitHub description.
  3. Rewrites only the block between the claude_bot markers. The first run
     wraps the existing "## Our Repositories" section in the markers and
     points old SmartFDD links at the org.
  4. Opens (or refreshes) a PR on the profile repo. No PR if nothing changed.

Usage:
  org_readme.py                       Open/refresh the PR.
  org_readme.py --dry-run [--out D]   Write README.md + README.diff to D
                                      (default ./readme-bot-out), no writes.

Env vars:
  README_BOT_ORG      org login (default: FSU-FAC-BAS)
  PROFILE_REPO        repo holding the profile (default: <org>/.github)
  PROFILE_PATH        README path in it (default: profile/README.md)
  ORG_READ_TOKEN      token that can list the org's private repos
                      (falls back to GH_TOKEN)
  GH_TOKEN            token with contents + pull-requests write on PROFILE_REPO
  FSU_AI_API_KEY      FSU APIM subscription key (optional; no key = no AI)
  README_BOT_MODEL    Claude model id (default: claude-sonnet-4-6)
"""
import argparse
import difflib
import os
import re
from pathlib import Path

from common import (
    BotError, ask_claude, fail, gh_file, gh_get_all, gh_request, model_from_env,
    open_or_update_pr, warn,
)

START = "<!-- claude_bot:repos:start -->"
END = "<!-- claude_bot:repos:end -->"
CATEGORIES = [
    "Core Services",
    "Frontend Applications",
    "Automation & Scripts",
    "Data & Analytics",
    "Integration & Configuration",
    "Documentation & Onboarding",
]
OTHER = "Other"
ARCHIVED = "Archived"
ROW_RE = re.compile(r"^\|\s*\[([^\]]+)\]\([^)]*\)\s*\|\s*(.*?)\s*\|\s*$")
README_EXCERPT = 3_000

SYSTEM_PROMPT = """You maintain the repository catalog in the GitHub org profile of the FSU Facilities
Building Automation Systems (BAS) software team.

For each new repository you get its name, GitHub description, language, topics and
the start of its README. Place it in exactly one category and write a short catalog
description: plain English, at most 12 words, no trailing period, no Markdown, no
marketing words. Base it only on the facts given.

Categories: {categories}. Use "Other" only when none fits.

Reply with only a JSON object:
{{"repos": {{"<repo name>": {{"category": "<category>", "description": "<text>"}}}}}}"""


def parse_catalog(text):
    """{lowercase repo name: (category, description)} from the catalog tables."""
    if START in text and END in text:
        text = text[text.index(START):text.index(END)]
    known, category = {}, OTHER
    for line in text.splitlines():
        if line.startswith("### "):
            category = line[4:].strip()
        match = ROW_RE.match(line)
        if match:
            known[match.group(1).strip().lower()] = (category, match.group(2).replace("\\|", "|"))
    return known


def list_repos(org, token):
    repos = gh_get_all(f"/orgs/{org}/repos?type=all&sort=full_name", token, 1000)
    return [{
        "name": r["name"],
        "full_name": r["full_name"],
        "description": (r.get("description") or "").strip(),
        "language": r.get("language") or "",
        "topics": r.get("topics") or [],
        "archived": r.get("archived", False),
    } for r in repos]


def readme_excerpt(full_name, token):
    try:
        text = gh_request("GET", f"/repos/{full_name}/readme", token, accept="application/vnd.github.raw")
    except BotError:
        return ""
    return text[:README_EXCERPT]


def classify_new(new, token, api_key, model):
    """{name: (category, description)} for repos not yet in the catalog."""
    result = {r["name"]: (OTHER, r["description"] or "-") for r in new}
    if not new:
        return result
    if not api_key:
        warn("FSU_AI_API_KEY is not set; new repos go under Other with their GitHub description.")
        return result
    blocks = []
    for r in new:
        blocks.append("\n".join([
            f"## {r['name']}",
            f"Description: {r['description'] or '(none)'}",
            f"Language: {r['language'] or '(unknown)'}",
            f"Topics: {', '.join(r['topics']) or '(none)'}",
            "README start:",
            readme_excerpt(r["full_name"], token) or "(no README)",
        ]))
    try:
        reply = ask_claude(
            SYSTEM_PROMPT.format(categories=", ".join(f'"{c}"' for c in CATEGORIES + [OTHER])),
            "\n\n".join(blocks), api_key, model,
        )
    except Exception as e:  # policy: any AI failure falls back to the plain catalog
        warn(f"AI classification failed ({type(e).__name__}: {e}); using GitHub descriptions.")
        return result
    for name, entry in (reply.get("repos") or {}).items():
        if name not in result or not isinstance(entry, dict):
            continue
        category = str(entry.get("category", "")).strip()
        description = " ".join(str(entry.get("description", "")).split())
        result[name] = (
            category if category in CATEGORIES else OTHER,
            description or result[name][1],
        )
    return result


def cell(text):
    return " ".join(text.split()).replace("|", "\\|") or "-"


def render_catalog(org, entries):
    """entries: [(name, category, description)]."""
    out = [START, "## Our Repositories", ""]
    for category in CATEGORIES + [OTHER, ARCHIVED]:
        rows = sorted((e for e in entries if e[1] == category), key=lambda e: e[0].lower())
        if not rows:
            continue
        out += [f"### {category}", "", "| Repository | Description |", "|------------|-------------|"]
        out += [f"| [{name}](https://github.com/{org}/{name}) | {cell(desc)} |" for name, _, desc in rows]
        out.append("")
    out.append(END)
    return "\n".join(out)


def splice(readme, block, org):
    """Replace the marked block. On the first run, mark the existing section."""
    if START in readme and END in readme:
        head, rest = readme.split(START, 1)
        return head + block + rest.split(END, 1)[1]
    readme = readme.replace("github.com/SmartFDD/", f"github.com/{org}/")
    readme = readme.replace("raw.githubusercontent.com/SmartFDD/", f"raw.githubusercontent.com/{org}/")
    lines = readme.split("\n")
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == "## Our Repositories")
    except StopIteration:
        return readme.rstrip("\n") + "\n\n" + block + "\n"
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[:start] + [block, ""] + lines[end:])


def run(args):
    org = os.environ.get("README_BOT_ORG", "FSU-FAC-BAS")
    profile_repo = os.environ.get("PROFILE_REPO") or f"{org}/.github"
    profile_path = os.environ.get("PROFILE_PATH", "profile/README.md")
    write_token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
    read_token = os.environ.get("ORG_READ_TOKEN") or write_token

    current, _ = gh_file(profile_repo, profile_path, "HEAD", write_token)
    if current is None:
        raise BotError(f"{profile_repo}/{profile_path} not found")
    known = parse_catalog(current)

    repos = list_repos(org, read_token)
    if not any(r["name"] != ".github" for r in repos):
        raise BotError(f"No repos listed for {org}; check ORG_READ_TOKEN")
    new = [r for r in repos if r["name"].lower() not in known]
    placed = classify_new(new, read_token, os.environ.get("FSU_AI_API_KEY", ""), model_from_env())

    entries = []
    for r in repos:
        category, description = known.get(r["name"].lower()) or placed[r["name"]]
        if r["archived"]:
            category = ARCHIVED
        elif category == ARCHIVED:  # unarchived since the last run
            category = OTHER
        entries.append((r["name"], category, description))

    updated = splice(current, render_catalog(org, entries), org)
    gone = sorted(set(known) - {r["name"].lower() for r in repos})
    summary = (f"{len(repos)} repos listed, {len(new)} new"
               + (f" ({', '.join(r['name'] for r in new)})" if new else "")
               + (f", {len(gone)} removed ({', '.join(gone)})" if gone else ""))

    if args.dry_run:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "README.md").write_text(updated)
        diff = difflib.unified_diff(current.splitlines(True), updated.splitlines(True),
                                    f"a/{profile_path}", f"b/{profile_path}")
        (out / "README.diff").write_text("".join(diff))
        return f"dry run: {summary}; written to {out}/"

    body = "\n".join([
        f"Automated update of the org repository catalog by claude_bot.",
        "",
        f"- {summary}",
        "- Only the block between the `claude_bot:repos` markers is generated; edit categories"
        " or descriptions there and the bot keeps your edits on later runs.",
        "",
        "Generated by `claude-bot/org_readme.py` in FSU-FAC-BAS/.github.",
    ])
    url = open_or_update_pr(profile_repo, profile_path, updated, "Update org repository catalog", body, write_token)
    return f"{summary}; {url or 'catalog already up to date'}"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="write the README to --out instead of opening a PR")
    parser.add_argument("--out", default="readme-bot-out", help="dry-run output directory")
    args = parser.parse_args()
    try:
        print(run(args))
    except BotError as e:
        fail(str(e))


if __name__ == "__main__":
    main()
