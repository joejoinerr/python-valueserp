from unittest import mock

import pytest

from valueserp import const
from valueserp.client import GoogleClient
from valueserp.credentials import Credentials
from valueserp.serp import WebSERP


@pytest.fixture(scope="module")
async def client():
    creds = Credentials('TESTKEY')
    with GoogleClient(creds) as client:
        yield client


class TestGoogleClient:
    @pytest.mark.asyncio
    async def test_search_success(self, client: GoogleClient):
        with mock.patch("valueserp.GoogleClient._request") as mock_request:
            mock_request.return_value = '{"result": "success"}'
            result = client.search({'q': 'test'})
            mock_request.assert_called_once_with(
                const.API_PATH["search"], params={'q': 'test'}
            )
            assert result == {'result': 'success'}


    @pytest.mark.asyncio
    async def test_web_search_success(self, client: GoogleClient):
        with mock.patch("valueserp.GoogleClient.search") as mock_search:
            mock_search.return_value = {'result': 'success'}
            result = client.web_search('test')
            mock_search.assert_called_once_with(params={'q': 'test', 'location': None})
            assert isinstance(result, WebSERP)
            assert result.raw == {'result': 'success'}


    @pytest.mark.asyncio
    async def test_site_web_search_success(self, client: GoogleClient):
        with mock.patch("valueserp.GoogleClient.search") as mock_search:
            mock_search.return_value = {'result': 'success'}
            result = client.web_search('test', site='example.com')
            mock_search.assert_called_once_with(
                params={'q': 'site:example.com test', 'location': None},
            )
            assert isinstance(result, WebSERP)
            assert result.raw == {'result': 'success'}
