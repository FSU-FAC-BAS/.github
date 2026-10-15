#!/usr/bin/env python3
"""
claude_bot: propose README fixes after a push changes the code.

Built to run as a GitHub Actions step on a push (for example to `main`) on a
self-hosted runner inside the FSU network:

  1. Collects the commits and diff in BEFORE..AFTER through the GitHub API.
     Skips pushes that only touch docs, and pushes made by claude_bot.
  2. Sends Claude (through the FSU Azure APIM gateway) the current README, the
     diff and the file tree. Claude returns JSON saying whether the README is
     now wrong or missing something, and the corrected README.
  3. Rejects edits that drop a `## ` section or shrink the README below 60%.
  4. Opens (or refreshes) a PR against the pushed branch.

If the AI call fails the script warns and exits 0: no README is better than a
wrong one.

Usage:
  repo_readme.py                       Run for the push described by the env.
  repo_readme.py --dry-run [--out D]   Write README.md + README.diff to D
                                       (default ./readme-bot-out), no writes.

Env vars:
  GITHUB_REPOSITORY   owner/name (required)
  GH_TOKEN            token with contents + pull-requests write on the repo
  GITHUB_REF_NAME     branch that was pushed; the PR targets it (default: repo default)
  BEFORE, AFTER       push range; AFTER defaults to GITHUB_SHA
  README_PATH         README to maintain (default: README.md)
  FSU_AI_API_KEY      FSU APIM subscription key (required to propose changes)
  README_BOT_MODEL    Claude model id (default: claude-sonnet-4-6)
"""
import argparse
import difflib
import os
import re
from pathlib import Path

from common import (
    BOT_EMAIL, BOT_NAME, BotError, ask_claude, fail, gh_file, gh_get, model_from_env,
    open_or_update_pr, warn,
)

ZERO_SHA = "0" * 40
SHA_RE = re.compile(r"[0-9a-f]{40}")
DIFF_LIMIT = 80_000
TREE_LIMIT = 400
MIN_LENGTH_RATIO = 0.6
DOC_RE = re.compile(r"(^|/)(README[^/]*|CHANGELOG[^/]*|LICENSE[^/]*|[^/]+\.md|docs/.*)$", re.I)
TREE_SKIP_RE = re.compile(r"(^|/)(node_modules|\.git|dist|build|\.next|__pycache__|\.venv|venv|vendor)(/|$)")

SYSTEM_PROMPT = """You keep a repository's README accurate for the FSU Facilities BAS software team.

You get the current README, the file tree, and the commits and diff of a push.
Decide whether the push makes the README wrong or leaves out something a developer
needs: setup or install steps, commands and scripts, environment variables and
config, ports, API endpoints, project structure, dependencies, features.

Rules:
- Change only what the push makes wrong or missing. Keep every other line exactly
  as it is, including headings, badges, wording, order and formatting.
- Do not remove sections. Do not rewrite for style. Do not add marketing text.
- Use only facts shown in the diff or tree. If unsure, do not change it.
- Most pushes need no README change. Say so when that is the case.

Reply with only a JSON object:
{"update": true|false, "reason": "<one or two plain sentences on what changed and why>",
 "readme": "<the full corrected README when update is true, else empty>"}"""


def collect(repo, before, after, token):
    """{'commits': [...], 'files': [...]} for the push."""
    if before and before != ZERO_SHA:
        try:
            compare = gh_get(f"/repos/{repo}/compare/{before}...{after}", token)
            return {
                "commits": [c["commit"] for c in compare.get("commits", [])],
                "files": compare.get("files", []),
            }
        except BotError as e:
            if e.status not in (404, 422):  # unknown BEFORE after a force-push
                raise
            warn(f"Could not compare {before[:7]}...{after[:7]} ({e.status}); using the pushed commit only.")
    head = gh_get(f"/repos/{repo}/commits/{after}", token)
    return {"commits": [head["commit"]], "files": head.get("files", [])}


def file_tree(repo, sha, token):
    tree = gh_get(f"/repos/{repo}/git/trees/{sha}?recursive=1", token).get("tree", [])
    paths = [t["path"] for t in tree if t["type"] == "blob" and not TREE_SKIP_RE.search(t["path"])]
    return paths[:TREE_LIMIT] + ([f"... ({len(paths) - TREE_LIMIT} more)"] if len(paths) > TREE_LIMIT else [])


def build_input(readme, change, tree):
    lines = [
        "Current README:", "<<<README", readme, "README>>>", "",
        "File tree:", *tree, "",
        "Commits:", *[f"- {c['message'].splitlines()[0]}" for c in change["commits"][:50]], "",
        "Files changed:",
        *[f"- {f.get('status', 'modified')} {f['filename']}" for f in change["files"][:200]], "",
        "Diff (truncated):",
    ]
    budget = DIFF_LIMIT
    for f in change["files"]:
        if budget <= 0 or not f.get("patch"):
            continue
        chunk = f"--- {f['filename']}\n{f['patch']}\n"
        lines.append(chunk[:budget])
        budget -= len(chunk)
    return "\n".join(lines)


def headings(text):
    return {line.strip() for line in text.splitlines() if line.startswith("## ")}


def check_edit(old, new):
    """None if the proposed README is safe to propose, else why not."""
    if len(new) < len(old) * MIN_LENGTH_RATIO:
        return f"proposed README is {len(new)} chars vs {len(old)} (below {MIN_LENGTH_RATIO:.0%})"
    dropped = headings(old) - headings(new)
    if dropped:
        return f"proposed README drops sections: {', '.join(sorted(dropped))}"
    return None


def run(args):
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", repo):
        raise BotError("GITHUB_REPOSITORY must be set to owner/name")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
    readme_path = os.environ.get("README_PATH", "README.md")
    after = os.environ.get("AFTER") or os.environ.get("GITHUB_SHA", "")
    before = os.environ.get("BEFORE", "")
    if after == ZERO_SHA:
        return "skipped: branch was deleted"
    if not SHA_RE.fullmatch(after) or (before and not SHA_RE.fullmatch(before)):
        raise BotError("BEFORE/AFTER must be full 40-character commit SHAs")

    change = collect(repo, before, after, token)
    if not change["files"]:
        return "skipped: no file changes"
    if all(DOC_RE.search(f["filename"]) for f in change["files"]):
        return "skipped: push only changed docs"
    head = change["commits"][-1]
    if BOT_NAME in (head["author"]["name"], head["committer"]["name"]) or head["author"].get("email") == BOT_EMAIL:
        return "skipped: push was made by claude_bot"

    readme, _ = gh_file(repo, readme_path, after, token)
    if readme is None:
        warn(f"{readme_path} does not exist; claude_bot only updates existing READMEs.")
        return "skipped: no README"

    api_key = os.environ.get("FSU_AI_API_KEY", "")
    if not api_key:
        warn("FSU_AI_API_KEY is not set; no README check.")
        return "skipped: no AI key"
    try:
        reply = ask_claude(SYSTEM_PROMPT, build_input(readme, change, file_tree(repo, after, token)),
                           api_key, model_from_env(), max_tokens=16000)
    except Exception as e:  # policy: never propose a README without the AI
        warn(f"AI README check failed ({type(e).__name__}: {e}); no PR opened.")
        return "skipped: AI failed"

    reason = " ".join(str(reply.get("reason", "")).split()) or "README out of date after recent changes."
    new = str(reply.get("readme") or "")
    if not reply.get("update") or not new.strip():
        return f"README is current: {reason}"
    if not new.endswith("\n"):
        new += "\n"
    if new == readme:
        return "README is current (no text change proposed)"
    problem = check_edit(readme, new)
    if problem:
        warn(f"Rejected AI README edit: {problem}")
        return "skipped: unsafe edit"

    if args.dry_run:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "README.md").write_text(new)
        diff = difflib.unified_diff(readme.splitlines(True), new.splitlines(True),
                                    f"a/{readme_path}", f"b/{readme_path}")
        (out / "README.diff").write_text("".join(diff))
        return f"dry run: {reason} Written to {out}/"

    body = "\n".join([
        reason, "",
        f"Proposed by claude_bot after the push `{(before or after)[:7]}..{after[:7]}`.",
        "Review the diff: the bot only sees the code, not your intent. Close the PR to discard it.",
        "",
        "Generated by `claude-bot/repo_readme.py` in FSU-FAC-BAS/.github.",
    ])
    url = open_or_update_pr(repo, readme_path, new, f"Update {readme_path} for recent changes", body, token,
                            base=os.environ.get("GITHUB_REF_NAME") or None)
    return f"{reason} {url or '(already up to date)'}"


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
