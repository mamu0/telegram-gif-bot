"""
Unit tests for the GiphyAPI class.
"""
import pytest
import requests
from unittest.mock import patch, MagicMock

from main import GiphyAPI


FAKE_GIF = {
    "id": "abc123",
    "title": "Test GIF",
    "images": {
        "fixed_height": {"url": "https://example.com/gif.gif", "width": "200", "height": "150"},
        "fixed_height_small": {"url": "https://example.com/gif_small.gif", "width": "100", "height": "75"},
        "fixed_height_small_still": {"url": "https://example.com/gif_still.gif"},
    },
}


def _mock_response(data: list) -> MagicMock:
    """Build a mock requests.Response returning the given data list."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": data}
    mock_resp.raise_for_status = MagicMock()
    return mock_resp


class TestGiphyAPISearch:
    def setup_method(self):
        self.api = GiphyAPI("test_key")

    def test_search_returns_results(self):
        with patch("requests.get", return_value=_mock_response([FAKE_GIF])):
            result = self.api.search("cat")
        assert len(result) == 1
        assert result[0]["id"] == "abc123"

    def test_search_passes_query_and_limit(self):
        with patch("requests.get", return_value=_mock_response([])) as mock_get:
            self.api.search("dog", limit=5, offset=10)
        call_params = mock_get.call_args[1]["params"]
        assert call_params["q"] == "dog"
        assert call_params["limit"] == 5
        assert call_params["offset"] == 10

    def test_search_returns_empty_list_on_network_error(self):
        with patch("requests.get", side_effect=requests.exceptions.RequestException("timeout")):
            result = self.api.search("cat")
        assert result == []

    def test_search_returns_empty_list_on_http_error(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("429")
        with patch("requests.get", return_value=mock_resp):
            result = self.api.search("cat")
        assert result == []

    def test_search_retries_without_lang_when_empty(self):
        """When lang is set and search returns nothing, it should retry without lang."""
        import main as bot_main
        original_lang = bot_main.GIPHY_LANGUAGE
        bot_main.GIPHY_LANGUAGE = "it"

        try:
            call_count = 0

            def fake_get(*args, **kwargs):
                nonlocal call_count
                call_count += 1
                # First call (with lang): empty; second call (without lang): one result
                data = [] if call_count == 1 else [FAKE_GIF]
                return _mock_response(data)

            with patch("requests.get", side_effect=fake_get):
                result = self.api.search("cat")

            assert call_count == 2
            assert len(result) == 1
        finally:
            bot_main.GIPHY_LANGUAGE = original_lang


class TestGiphyAPITrending:
    def setup_method(self):
        self.api = GiphyAPI("test_key")

    def test_trending_returns_results(self):
        with patch("requests.get", return_value=_mock_response([FAKE_GIF])):
            result = self.api.trending()
        assert len(result) == 1
        assert result[0]["title"] == "Test GIF"

    def test_trending_passes_limit_and_offset(self):
        with patch("requests.get", return_value=_mock_response([])) as mock_get:
            self.api.trending(limit=5, offset=20)
        call_params = mock_get.call_args[1]["params"]
        assert call_params["limit"] == 5
        assert call_params["offset"] == 20

    def test_trending_returns_empty_list_on_error(self):
        with patch("requests.get", side_effect=requests.exceptions.RequestException("timeout")):
            result = self.api.trending()
        assert result == []


class TestWebhookEndpoint:
    def setup_method(self):
        from main import app
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health_check(self):
        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.get_json()["status"] == "ok"

    def test_root_endpoint(self):
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "running"

    def test_webhook_rejects_empty_body(self):
        response = self.client.post(
            "/webhook",
            data="not-json",
            content_type="text/plain",
        )
        assert response.status_code == 400

    def test_webhook_rejects_invalid_secret(self):
        import main as bot_main
        original = bot_main.WEBHOOK_SECRET_TOKEN
        bot_main.WEBHOOK_SECRET_TOKEN = "correct-secret"

        try:
            response = self.client.post(
                "/webhook",
                json={"update_id": 1},
                headers={"X-Telegram-Bot-Api-Secret-Token": "wrong-secret"},
            )
            assert response.status_code == 401
        finally:
            bot_main.WEBHOOK_SECRET_TOKEN = original

    def test_webhook_accepts_valid_secret(self):
        import main as bot_main
        original = bot_main.WEBHOOK_SECRET_TOKEN
        bot_main.WEBHOOK_SECRET_TOKEN = "correct-secret"

        try:
            with patch("main.Update.de_json", return_value=MagicMock(inline_query=None, message=None)):
                response = self.client.post(
                    "/webhook",
                    json={"update_id": 1},
                    headers={"X-Telegram-Bot-Api-Secret-Token": "correct-secret"},
                )
            assert response.status_code == 200
        finally:
            bot_main.WEBHOOK_SECRET_TOKEN = original
