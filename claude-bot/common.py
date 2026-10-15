"""
Shared helpers for claude_bot: GitHub REST calls, the FSU AI
gateway, and the "commit one file to a bot branch and open/refresh a PR" flow.

Standard library only (same as ci/merge-notify in fsu-ai-dev-skills), so it runs on a bare
self-hosted runner.
"""
import base64
import http.client
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

GITHUB_API = "https://api.github.com"
GATEWAY = "https://apim-n1ai-usc-5c27e2ff4.azure-api.net/anthropic"
DEFAULT_MODEL = "claude-sonnet-4-6"
BOT_NAME = "claude_bot"
BOT_EMAIL = "claude-bot@users.noreply.github.com"
BOT_BRANCH_PREFIX = "claude-bot/"


class BotError(Exception):
    def __init__(self, message, status=None):
        super().__init__(message)
        self.status = status


def in_actions():
    return os.environ.get("GITHUB_ACTIONS") == "true"


def warn(message):
    print(f"::warning::{message}" if in_actions() else f"WARNING: {message}", file=sys.stderr)


def fail(message):
    print(f"::error::{message}" if in_actions() else f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def model_from_env():
    return os.environ.get("README_BOT_MODEL") or DEFAULT_MODEL


# --------------------------------------------------------------------------- #
# GitHub
# --------------------------------------------------------------------------- #

def gh_request(method, path, token, body=None, accept="application/vnd.github+json"):
    request = urllib.request.Request(
        path if path.startswith("http") else f"{GITHUB_API}{path}",
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={
            "Accept": accept,
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Content-Type": "application/json"} if body is not None else {}),
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
    except urllib.error.HTTPError as e:
        raise BotError(f"GitHub API {method} {path} returned {e.code}: {e.read()[:300]!r}", status=e.code)
    except urllib.error.URLError as e:
        raise BotError(f"GitHub API {method} {path} unreachable: {e.reason}")
    except (OSError, http.client.HTTPException) as e:
        raise BotError(f"GitHub API {method} {path} failed: {type(e).__name__}: {e}")
    if accept.endswith(".raw"):
        return raw.decode("utf-8", errors="replace")
    try:
        return json.loads(raw) if raw else None
    except ValueError as e:
        raise BotError(f"GitHub API {method} {path} returned non-JSON: {e}")


def gh_get(path, token):
    return gh_request("GET", path, token)


def gh_get_all(path, token, limit):
    """Follow ?page= until a short page or `limit` items."""
    items, page = [], 1
    sep = "&" if "?" in path else "?"
    while len(items) < limit:
        batch = gh_get(f"{path}{sep}per_page=100&page={page}", token)
        items.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return items[:limit]


def gh_file(repo, path, ref, token):
    """(text, blob sha) of a file, or (None, None) when it does not exist."""
    quoted = urllib.parse.quote(path)
    try:
        meta = gh_get(f"/repos/{repo}/contents/{quoted}?ref={urllib.parse.quote(ref)}", token)
    except BotError as e:
        if e.status == 404:
            return None, None
        raise
    if meta.get("encoding") == "base64":
        return base64.b64decode(meta["content"]).decode("utf-8", errors="replace"), meta["sha"]
    # Files over 1 MB come back without content; fetch the raw blob instead.
    text = gh_request("GET", f"/repos/{repo}/contents/{quoted}?ref={urllib.parse.quote(ref)}", token,
                      accept="application/vnd.github.raw")
    return text, meta["sha"]


def open_or_update_pr(repo, path, content, title, body, token, base=None, branch=None):
    """Put `content` at `path` on a bot branch cut fresh from `base` and open a
    PR, or refresh the bot's open PR. The bot owns the branch: it is reset on
    every run. Returns the PR URL, or None when `base` already has `content`."""
    info = gh_get(f"/repos/{repo}", token)
    base = base or info["default_branch"]
    branch = branch or f"{BOT_BRANCH_PREFIX}readme-{base.replace('/', '-')}"
    owner = repo.split("/")[0]
    existing = gh_get(f"/repos/{repo}/pulls?state=open&base={urllib.parse.quote(base)}"
                      f"&head={urllib.parse.quote(f'{owner}:{branch}')}", token)

    current, _ = gh_file(repo, path, base, token)
    if current == content:
        if existing:
            gh_request("PATCH", f"/repos/{repo}/pulls/{existing[0]['number']}", token, {"state": "closed"})
            return f"up to date; closed stale PR {existing[0]['html_url']}"
        return None

    base_sha = gh_get(f"/repos/{repo}/git/ref/heads/{urllib.parse.quote(base)}", token)["object"]["sha"]
    try:
        gh_request("PATCH", f"/repos/{repo}/git/refs/heads/{branch}", token, {"sha": base_sha, "force": True})
    except BotError as e:
        if e.status not in (404, 422):
            raise
        gh_request("POST", f"/repos/{repo}/git/refs", token, {"ref": f"refs/heads/{branch}", "sha": base_sha})

    _, file_sha = gh_file(repo, path, branch, token)
    gh_request("PUT", f"/repos/{repo}/contents/{urllib.parse.quote(path)}", token, {
        "message": f"docs: {title}",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": branch,
        "committer": {"name": BOT_NAME, "email": BOT_EMAIL},
        **({"sha": file_sha} if file_sha else {}),
    })

    if existing:
        pr = gh_request("PATCH", f"/repos/{repo}/pulls/{existing[0]['number']}", token, {"title": title, "body": body})
    else:
        pr = gh_request("POST", f"/repos/{repo}/pulls", token,
                        {"title": title, "body": body, "head": branch, "base": base})
    return pr["html_url"]


# --------------------------------------------------------------------------- #
# FSU AI gateway
# --------------------------------------------------------------------------- #

def parse_json_object(text):
    start = text.find("{")
    if start < 0:
        raise BotError("AI reply had no JSON object")
    try:
        data, _ = json.JSONDecoder().raw_decode(text[start:])
    except ValueError as e:
        raise BotError(f"AI reply JSON did not parse: {e}")
    if not isinstance(data, dict):
        raise BotError("AI reply JSON was not an object")
    return data


def ask_claude(system, user, api_key, model, max_tokens=4000):
    """One Messages API call through the FSU APIM gateway; returns the JSON
    object in the reply."""
    request = urllib.request.Request(
        f"{GATEWAY}/v1/messages",
        data=json.dumps({
            "model": model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }).encode(),
        method="POST",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            reply = json.load(response)
    except urllib.error.HTTPError as e:
        raise BotError(f"FSU AI gateway returned {e.code}")
    except (urllib.error.URLError, TimeoutError) as e:
        raise BotError(f"FSU AI gateway unreachable: {e}")
    if reply.get("stop_reason") == "max_tokens":
        raise BotError("AI reply was cut off at max_tokens")
    text = "".join(b.get("text", "") for b in reply.get("content", []) if b.get("type") == "text")
    return parse_json_object(text)
