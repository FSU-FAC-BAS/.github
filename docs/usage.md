<p align="center">
  <img src="./assets/fsu-facilities-logo.png" alt="FSU Facilities" width="400">
</p>

# .github — Usage Guide

> Last updated: 2026-10-15

## Quick Start

```bash
# See profile/README.md for org profile
```

## Common Operations

### claude_bot: README updates in CI

`claude-bot/` keeps READMEs current and proposes every change as a pull
request for a person to review. It never pushes to a protected branch. Like
merge-notify in fsu-ai-dev-skills, it calls Claude through the FSU APIM gateway, so it must run on a
**self-hosted runner inside the FSU network**. Scripts and workflows both live
in this repo; it is public, so calling repos fetch the scripts without a token.

| Script | Runs | What it does |
|---|---|---|
| `org_readme.py` | Weekly + manual, `claude-bot-org-readme.yml` | Lists all org repos and rewrites the catalog between the `claude_bot:repos` markers in `profile/README.md`. Repos already listed keep their category and description; new repos are placed and described by Claude; archived repos move to "Archived"; deleted repos drop out. |
| `repo_readme.py` | On push, reusable `claude-bot-readme.yml` | Sends Claude the README, the push diff and the file tree. If the push makes the README wrong or incomplete, opens a PR against the pushed branch with the fix. |

Safety rules:

- Each script owns one branch (`claude-bot/readme-<base>`), resets it from the
  base on every run, and refreshes its own open PR instead of opening another.
  The org script closes its PR when the catalog is already current.
- `repo_readme.py` skips pushes that only change docs and pushes by
  `claude_bot`, and rejects AI edits that drop a `## ` section or shrink the
  README below 60%. If the AI call fails it opens nothing.
- `org_readme.py` without the AI still updates the catalog; new repos go under
  "Other" with their GitHub description. Edit the generated tables freely: the
  bot keeps your categories and descriptions on later runs.

| Env var | Used by | Default / notes |
|---|---|---|
| `GH_TOKEN` | both | `${{ github.token }}` with `contents: write`, `pull-requests: write` |
| `FSU_AI_API_KEY` | both | FSU APIM subscription key (org secret) |
| `README_BOT_MODEL` | both | `claude-sonnet-4-6` |
| `ORG_READ_TOKEN` | org | fine-grained token, **Metadata: read** on all org repos, so private repos are listed |
| `README_BOT_ORG`, `PROFILE_REPO`, `PROFILE_PATH` | org | `FSU-FAC-BAS`, `<org>/.github`, `profile/README.md` |
| `GITHUB_REPOSITORY`, `BEFORE`, `AFTER`, `GITHUB_REF_NAME` | repo | set from the push event |
| `README_PATH` | repo | `README.md` |

One-time org setup (admin):

1. Org secrets `FSU_AI_API_KEY` and `ORG_READER` (passed as `ORG_READ_TOKEN`), with repository access
   that includes `.github` (public repos are often left out by default).
2. Org variable `README_BOT_RUNNER` with the FSU runner labels as JSON, for
   example `["self-hosted","fsu"]` (default `["self-hosted"]`).
3. Settings → Actions → General → **Allow GitHub Actions to create and approve
   pull requests**.

Turn it on in a repo by adding `.github/workflows/claude-bot.yml`:

```yaml
on:
  push:
    branches: [main]
jobs:
  readme:
    uses: FSU-FAC-BAS/.github/.github/workflows/claude-bot-readme.yml@main
    secrets: inherit
    permissions:
      contents: write
      pull-requests: write
    # with:
    #   runner: '["self-hosted","fsu"]'
```

Preview locally (from the FSU network for the AI part) without writing anything:

```bash
cd claude-bot
GH_TOKEN="$(gh auth token)" FSU_AI_API_KEY=<key> python3 org_readme.py --dry-run
GITHUB_REPOSITORY=FSU-FAC-BAS/<repo> GH_TOKEN="$(gh auth token)" FSU_AI_API_KEY=<key> \
  BEFORE=<sha> AFTER=<sha> python3 repo_readme.py --dry-run
```

Both write `README.md` and `README.diff` to `./readme-bot-out/`.

## API Reference

[To be documented]

## Examples

### [To be documented]

```[To be documented]
[To be documented]
```

## Scripts & Commands

| Command | Description |
|---------|-------------|
| `python3 claude-bot/org_readme.py --dry-run` | Preview the org repository catalog update |
| `python3 claude-bot/repo_readme.py --dry-run` | Preview a README fix for a push range |

## Related Documentation

- [Architecture](./architecture.md)
- [Setup Guide](./setup.md)
- [Changelog](./CHANGELOG.md)
