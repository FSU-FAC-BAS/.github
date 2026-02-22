<p align="center">
  <img src="docs/assets/fsu-facilities-logo.png" alt="FSU Facilities" width="400">
</p>

# Contributing to .github

Thank you for your interest in contributing to **.github**, a SmartFDD project.

## Getting Started

1. Clone the repository
2. Follow the [Setup Guide](docs/setup.md)
3. Create a feature branch from `main`

## Branch Naming Convention

Use the following format:

```
<type>/<short-description>
```

| Type | Purpose |
|------|---------|
| `feature/` | New features |
| `fix/` | Bug fixes |
| `docs/` | Documentation changes |
| `refactor/` | Code refactoring |
| `test/` | Adding or updating tests |
| `chore/` | Maintenance tasks |

**Examples:**
- `feature/add-bacnet-discovery`
- `fix/connection-timeout`
- `docs/update-setup-guide`

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`

**Examples:**
- `feat(api): add device status endpoint`
- `fix(auth): resolve token refresh race condition`
- `docs(setup): update Docker instructions`

## Pull Request Process

1. Create a branch following the naming convention above
2. Make your changes with clear, atomic commits
3. Ensure all tests pass locally
4. Update documentation if your changes affect setup, usage, or architecture
5. Open a PR against `main` with:
   - Clear title following commit message format
   - Description of what changed and why
   - Link to related issues (if any)
6. Request review from at least one team member
7. Address review feedback
8. Squash-merge once approved

## Code Review Guidelines

- Be constructive and specific
- Approve when satisfied, request changes when blocking issues exist
- Focus on correctness, readability, and maintainability

## Documentation Requirements

All PRs must maintain documentation standards:
- `README.md` — Project overview
- `CONTRIBUTING.md` — This file
- `docs/architecture.md` — System design
- `docs/setup.md` — Installation & configuration
- `docs/usage.md` — How to use
- `docs/CHANGELOG.md` — Version history

CI will block merges to `main` if required docs are missing.

## Questions?

Reach out to the SmartFDD team or open a GitHub issue.
