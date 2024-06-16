"""Tests for the sync client."""

from unittest import mock

import httpx
import pytest
import respx

from valueserp import AsyncGoogleClient, const, exceptions
from valueserp.client import GoogleClient
from valueserp.const import DEFAULT_RETRIES, DEFAULT_TIMEOUT
from valueserp.credentials import Credentials
from valueserp.serp import WebSERP


@pytest.fixture(scope="module")
def creds():
    """Reusable credentials."""
    return Credentials("TESTKEY")


@pytest.fixture
def client(creds: Credentials):
    """Reusable async client."""
    with GoogleClient(creds) as client:
        yield client


@pytest.fixture(scope="module")
def respx_mock():
    """Reusable respx mock with preset base URL."""
    with respx.mock(base_url=const.ENDPOINT) as respx_mock:
        yield respx_mock


class TestGoogleClient:
    """Tests for the sync client."""

    def test_init(self, creds: Credentials):
        """Tests the initialization of the client."""
        client = AsyncGoogleClient(creds)
        assert client.credentials == creds
        assert isinstance(client._session, httpx.AsyncClient)
        assert client._session.base_url == const.ENDPOINT
        assert dict(client._session.params) == {"api_key": creds.api_key}
        assert client._session.timeout == httpx.Timeout(DEFAULT_TIMEOUT)
        assert client._session._transport._pool._retries == DEFAULT_RETRIES

    def test_close(self, creds: Credentials):
        """Tests the `close` method."""
        client = GoogleClient(creds)
        client.close()
        assert client._session.is_closed

    def test_enter_exit(self, creds: Credentials):
        """Tests the `__enter__` and `__exit__` methods."""
        with GoogleClient(creds) as client:
            assert not client._session.is_closed
        assert client._session.is_closed

    def test_request_success(self, client: GoogleClient, respx_mock: respx.Router):
        """Tests the `_request` method."""
        test_route = respx_mock.get(
            url=const.API_PATH["search"],
            params={"api_key": "TESTKEY", "q": "test"},
        ).respond(json={"result": "success"})
        response = client._request(const.API_PATH["search"], params={"q": "test"})
        assert response == '{"result": "success"}'
        assert test_route.called

    def test_request_request_error(
        self, client: GoogleClient, respx_mock: respx.Router
    ):
        """Tests that the `_request` method raises a RequestError properly."""
        test_route = respx_mock.get(
            url=const.API_PATH["search"],
            params={"api_key": "TESTKEY", "q": "test"},
        ).mock(side_effect=httpx.RequestError("Test error"))
        with pytest.raises(exceptions.RequestError):
            client._request(const.API_PATH["search"], params={"q": "test"})
        assert test_route.called

    def test_request_response_error(
        self, client: GoogleClient, respx_mock: respx.Router
    ):
        """Tests that the `_request` method raises a ResponseError properly."""
        test_route = respx_mock.get(
            url=const.API_PATH["search"],
            params={"api_key": "TESTKEY", "q": "test"},
        ).respond(status_code=429, json={"request_info": {"message": "Rate limited"}})
        with pytest.raises(exceptions.ResponseError) as exc_info:
            client._request(const.API_PATH["search"], params={"q": "test"})
        assert test_route.called
        assert exc_info.value.status_code == 429
        assert exc_info.value.response_message == "Rate limited"

    def test_search_success(self, client: GoogleClient):
        """Tests the `search` method."""
        with mock.patch("valueserp.GoogleClient._request") as mock_request:
            mock_request.return_value = '{"result": "success"}'
            result = client.search({"q": "test"})
            mock_request.assert_called_once_with(
                const.API_PATH["search"], params={"q": "test"}
            )
            assert result == {"result": "success"}

    def test_web_search_success(self, client: GoogleClient):
        """Tests the `web_search` method."""
        with mock.patch("valueserp.GoogleClient.search") as mock_search:
            mock_search.return_value = {"result": "success"}
            result = client.web_search("test")
            mock_search.assert_called_once_with(params={"q": "test", "location": None})
            assert isinstance(result, WebSERP)
            assert result.raw == {"result": "success"}

    def test_site_web_search_success(self, client: GoogleClient):
        """Tests the `web_search` method with a site parameter."""
        with mock.patch("valueserp.GoogleClient.search") as mock_search:
            mock_search.return_value = {"result": "success"}
            result = client.web_search("test", site="example.com")
            mock_search.assert_called_once_with(
                params={"q": "site:example.com test", "location": None},
            )
            assert isinstance(result, WebSERP)
            assert result.raw == {"result": "success"}
