"""Tests for the async client."""

from unittest import mock

import httpx
import pytest
import respx

from valueserp import const, exceptions
from valueserp.aclient import AsyncGoogleClient
from valueserp.credentials import Credentials
from valueserp.serp import WebSERP


@pytest.fixture(scope="module")
def creds():
    """Reusable credentials."""
    return Credentials("TESTKEY")


@pytest.fixture
async def client(creds: Credentials):
    """Reusable async client."""
    async with AsyncGoogleClient(creds) as client:
        yield client


@pytest.fixture(scope="module")
def respx_mock():
    """Reusable respx mock with preset base URL."""
    with respx.mock(base_url=const.ENDPOINT) as respx_mock:
        yield respx_mock


class TestAsyncGoogleClient:
    """Tests for the async client."""

    def test_init(self, creds: Credentials):
        """Tests the initialization of the client."""
        client = AsyncGoogleClient(creds)
        assert client.credentials == creds
        assert isinstance(client._session, httpx.AsyncClient)
        assert client._session.base_url == const.ENDPOINT
        assert dict(client._session.params) == {"api_key": creds.api_key}
        assert client._session.timeout == httpx.Timeout(5.0)
        assert client._session._transport._pool._retries == 3

    @pytest.mark.asyncio
    async def test_close(self, creds: Credentials):
        """Tests the `close` method."""
        client = AsyncGoogleClient(creds)
        await client.close()
        assert client._session.is_closed

    @pytest.mark.asyncio
    async def test_aenter_aexit(self, creds: Credentials):
        """Tests the `__aenter__` and `__aexit__` methods."""
        async with AsyncGoogleClient(creds) as client:
            assert not client._session.is_closed
        assert client._session.is_closed

    @pytest.mark.asyncio
    async def test_request_success(
        self, client: AsyncGoogleClient, respx_mock: respx.Router
    ):
        """Tests the `_request` method."""
        test_route = respx_mock.get(
            url=const.API_PATH["search"],
            params={"api_key": "TESTKEY", "q": "test"},
        ).respond(json={"result": "success"})
        response = await client._request(const.API_PATH["search"], params={"q": "test"})
        assert response == '{"result": "success"}'
        assert test_route.called

    @pytest.mark.asyncio
    async def test_request_request_error(
        self, client: AsyncGoogleClient, respx_mock: respx.Router
    ):
        """Tests that the `_request` method raises a RequestError properly."""
        test_route = respx_mock.get(
            url=const.API_PATH["search"],
            params={"api_key": "TESTKEY", "q": "test"},
        ).mock(side_effect=httpx.RequestError("Test error"))
        with pytest.raises(exceptions.RequestError):
            await client._request(const.API_PATH["search"], params={"q": "test"})
        assert test_route.called

    @pytest.mark.asyncio
    async def test_request_response_error(
        self, client: AsyncGoogleClient, respx_mock: respx.Router
    ):
        """Tests that the `_request` method raises a ResponseError properly."""
        test_route = respx_mock.get(
            url=const.API_PATH["search"],
            params={"api_key": "TESTKEY", "q": "test"},
        ).respond(status_code=429, json={"request_info": {"message": "Rate limited"}})
        with pytest.raises(exceptions.ResponseError) as exc_info:
            await client._request(const.API_PATH["search"], params={"q": "test"})
        assert test_route.called
        assert exc_info.value.status_code == 429
        assert exc_info.value.response_message == "Rate limited"

    @pytest.mark.asyncio
    async def test_search_success(self, client: AsyncGoogleClient):
        """Tests the `search` method."""
        with mock.patch("valueserp.AsyncGoogleClient._request") as mock_request:
            mock_request.return_value = '{"result": "success"}'
            result = await client.search({"q": "test"})
            mock_request.assert_called_once_with(
                const.API_PATH["search"], params={"q": "test"}
            )
            assert result == {"result": "success"}

    @pytest.mark.asyncio
    async def test_web_search_success(self, client: AsyncGoogleClient):
        """Tests the `web_search` method."""
        with mock.patch("valueserp.AsyncGoogleClient.search") as mock_search:
            mock_search.return_value = {"result": "success"}
            result = await client.web_search("test")
            mock_search.assert_called_once_with(params={"q": "test", "location": None})
            assert isinstance(result, WebSERP)
            assert result.raw == {"result": "success"}

    @pytest.mark.asyncio
    async def test_site_web_search_success(self, client: AsyncGoogleClient):
        """Tests the `web_search` method with a site parameter."""
        with mock.patch("valueserp.AsyncGoogleClient.search") as mock_search:
            mock_search.return_value = {"result": "success"}
            result = await client.web_search("test", site="example.com")
            mock_search.assert_called_once_with(
                params={"q": "site:example.com test", "location": None},
            )
            assert isinstance(result, WebSERP)
            assert result.raw == {"result": "success"}
