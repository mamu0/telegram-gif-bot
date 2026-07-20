# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Security
- Updated `gunicorn` 21.2.0 → 26.0.0 (fixes CVE-2026-1433, CVE-2026-1434)
- Updated `aiohttp` 3.11.10 → 3.14.1 (fixes 30+ CVEs)
- Updated `flask` 3.0.0 → 3.1.3 (fixes CVE-2026-2151)
- Updated `requests` 2.32.3 → 2.34.2 (fixes CVE-2026-1872, CVE-2026-2275)
- Updated `python-dotenv` 1.0.1 → 1.2.2 (fixes CVE-2026-2270)
- Updated `python-telegram-bot` 21.7 → 21.11.1
- Added optional `WEBHOOK_SECRET_TOKEN` env var: when set, every incoming
  webhook request is verified against the `X-Telegram-Bot-Api-Secret-Token`
  header sent by Telegram, preventing spoofed payloads

### Fixed
- Replaced bare `except:` clause with `except Exception:` in the inline query
  error handler
- Removed `config.py`: it was not imported by `main.py`, had different default
  values (`GIPHY_RATING='g'` vs `'pg-13'`), and duplicated validation logic
- Removed `utils.py`: none of its functions were imported anywhere in the
  codebase (dead code)
- Replaced `from typing import List` with built-in `list[dict]` (Python ≥ 3.9)

### Added
- GitHub Actions CI pipeline (`.github/workflows/ci.yml`) running `pip-audit`
  and `pytest` on every push and pull request
- `tests/test_bot.py`: unit tests for `GiphyAPI` (search, trending, error
  handling, language fallback) and the Flask webhook endpoint
- `tests/conftest.py`: pytest fixture that sets fake env vars so tests run
  without a real `.env` file

## [1.0.0] - Initial release

### Added
- Inline GIF search via Giphy API
- Webhook-based architecture (no polling)
- Flask web server with `/health` and `/` endpoints
- Trending GIFs shown when the query is empty
- Pagination support via Telegram's `next_offset`
- Docker and docker-compose support
- `/start` and `/help` commands
