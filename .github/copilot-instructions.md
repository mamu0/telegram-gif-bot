# Telegram GIF Bot — Repo Instructions

These rules apply to **every** change made to this repository.

## Language

All code must be written in English: variable names, function names, class names,
comments, docstrings, log messages, error messages, and commit descriptions.

## Code Structure

- All configuration is read via `os.getenv()` directly in `main.py`. `config.py` does not exist and must not be recreated.
- `utils.py` does not exist. Helper functions live inline in `main.py` or in `tests/`. Recreating it is only justified if at least 3 functions are reused by distinct modules.
- The bot uses a single `asyncio` event loop (`telegram_loop`) created at startup; all Telegram calls go through `run_async()`. Do not refactor to `asyncio.run()` without an explicit reason.

## Mandatory Checklist for Every Change

### Python code
- Every added import must be actually used; remove orphaned imports.
- Every defined function or class must be called somewhere; remove dead code.
- Do not duplicate existing logic (e.g. env var validation, logging setup).
- Never replace `except Exception` with a bare `except:`.
- A new environment variable must be added to `.env.example` **and** documented in `README.md`.

### Dependencies (`requirements.txt`)
- After every change run the audit: `~/.local/bin/pip-audit -r requirements.txt`
- No open CVE may remain before committing.
- Keep only direct dependencies — do not add transitive packages.

### Tests
- Always run: `pytest tests/ -v`
- All tests must pass. A new Flask endpoint or a new `GiphyAPI` method requires a corresponding test in `tests/test_bot.py`.

## Versioning

Schema `0.x.y`: increment `y` for fixes/security, `x` for new features. Do not move to `1.x`.

To update the CHANGELOG use the `/release-workflow` skill.
