---
name: release-workflow
description: "Use when releasing a new version of the bot, updating the CHANGELOG, tagging a release, or bumping the version number. Covers: commit creation, git-cliff changelog generation, version bump, git tag."
argument-hint: "version number (e.g. 0.0.3)"
---

# Release Workflow — Telegram GIF Bot

## When to Use

- A new version needs to be released (any version bump)
- The `CHANGELOG.md` needs to be updated with unreleased changes
- A git tag needs to be created for a version

## Prerequisites

Both checks must pass before proceeding:

```bash
# 1. No open CVEs
~/.local/bin/pip-audit -r requirements.txt

# 2. All tests green
pytest tests/ -v
```

If either fails, **stop and fix it first**.

## Commit Rules

All commits in this repo must follow these rules:

**Format:** `<type>: <short description in English>`

**Types and their CHANGELOG section:**

| Type | CHANGELOG section | When to use |
|------|-------------------|-------------|
| `feat:` | Added | New feature or behaviour |
| `fix:` | Fixed | Bug fix |
| `security:` | Security | Dependency update, auth fix, CVE patch |
| `refactor:` | Changed | Code change with no functional difference |
| `perf:` | Performance | Speed or efficiency improvement |
| `docs:` | Documentation | README, INSTALLATION, comments only |
| `chore:` | *(ignored)* | Release commits, tooling, config |
| `ci:` | *(ignored)* | CI/CD workflow changes |
| `test:` | *(ignored)* | Test-only changes |

**Strict rules:**
- Description must be in English.
- Never include `Co-authored-by` or any authorship trailer in the commit message.
- Use imperative mood: `add support for X`, not `added support for X`.
- Keep the subject line under 72 characters.

**The agent creates the commits.** When changes are ready, stage the relevant files and run the commit — do not ask the user to do it manually.

Example commits for common changes:
```
security: update aiohttp 3.11.10 → 3.14.1 (CVE-2026-2094..2113)
feat: add language fallback for Giphy search
fix: prevent 500 on malformed webhook payload
refactor: replace typing.List with built-in list type hint
docs: document WEBHOOK_SECRET_TOKEN in README
chore: release v0.0.3
```

## Release Procedure

### Step 1 — Determine the version

Schema `0.x.y`:
- **Patch** (`y`): bug fixes, security updates, refactoring with no new behaviour
- **Minor** (`x`): new backwards-compatible features
- Do not move to `1.x` without explicit discussion

### Step 2 — Review unreleased commits

```bash
git log --oneline $(git describe --tags --abbrev=0)..HEAD
```

Any unreleased commit with a non-conventional message that contains relevant changes
must be added manually to the CHANGELOG before running git-cliff.

### Step 3 — Generate the CHANGELOG with git-cliff

```bash
git cliff --unreleased --tag v<VERSION> --prepend CHANGELOG.md
```

Review the output: check that sections are correct and there are no duplicates or missing entries.

### Step 4 — Commit and tag

```bash
git add CHANGELOG.md
git commit -m "chore: release v<VERSION>"
git tag v<VERSION>
```

> The release commit uses `chore:` so git-cliff ignores it in future releases.

### Step 5 — Push

```bash
git push origin main --tags
```

The tag push triggers the CI pipeline (pip-audit + pytest). Verify both jobs pass.

## Version History

| Tag | Date | Notes |
|-----|------|-------|
| v0.0.1 | 2026-07-10 | Initial release |
| v0.0.2 | 2026-07-20 | Security updates, CI, tests, dead code removal |
| *(next)* | — | Use this workflow |

## git-cliff Reference

Configuration lives in [`cliff.toml`](../../cliff.toml) at the repo root.
To regenerate the entire CHANGELOG from scratch:

```bash
git cliff --output CHANGELOG.md
```

