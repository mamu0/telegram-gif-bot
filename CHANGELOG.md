# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.0.2] - 2026-07-20

### Security
- Updated `gunicorn` 21.2.0 → 26.0.0 (CVE-2026-1433, CVE-2026-1434)
- Updated `aiohttp` 3.11.10 → 3.14.1 (30+ CVEs resolved)
- Updated `flask` 3.0.0 → 3.1.3 (CVE-2026-2151)
- Updated `requests` 2.32.3 → 2.34.2 (CVE-2026-1872, CVE-2026-2275)
- Updated `python-dotenv` 1.0.1 → 1.2.2 (CVE-2026-2270)
- Updated `python-telegram-bot` 21.7 → 21.11.1
- Added optional `WEBHOOK_SECRET_TOKEN`: verifies every incoming request against
  the `X-Telegram-Bot-Api-Secret-Token` header sent by Telegram

### Added
- GitHub Actions CI pipeline (dependency security audit + automated tests)
- Unit tests in `tests/` covering `GiphyAPI` and Flask endpoints

### Fixed
- Removed dead code: `config.py` and `utils.py` (never imported anywhere)
- Replaced bare `except:` with `except Exception:`
- Used `get_json(silent=True)` to prevent 500 errors on malformed payloads
- Dockerfile `CMD` now uses gunicorn instead of Flask dev server
- Dockerfile exposed port aligned to app default (8000)

## [0.0.1] - 2026-07-10

### Added
- Initial release
- Inline GIF search via Giphy API
- Webhook-based architecture (no polling)
- Flask web server with `/health` and `/` status endpoints
- Trending GIFs when the query is empty
- Pagination via Telegram's `next_offset`
- `/start` and `/help` bot commands
- Docker and docker-compose support
