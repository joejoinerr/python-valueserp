from unittest import mock

import pytest

from valueserp import const
from valueserp.aclient import AsyncGoogleClient
from valueserp.credentials import Credentials
from valueserp.serp import WebSERP


@pytest.fixture(scope="module")
async def client():
    creds = Credentials('TESTKEY', auto_validate=False)
    async with AsyncGoogleClient(creds) as client:
        yield client


class TestAsyncGoogleClient:
    @pytest.mark.asyncio
    async def test_search_success(self, client: AsyncGoogleClient):
        with mock.patch("valueserp.AsyncGoogleClient._request") as mock_request:
            mock_request.return_value = '{"result": "success"}'
            result = await client.search({'q': 'test'})
            mock_request.assert_called_once_with(
                const.API_PATH["search"], params={'q': 'test'}
            )
            assert result == {'result': 'success'}


    @pytest.mark.asyncio
    async def test_web_search_success(self, client: AsyncGoogleClient):
        with mock.patch("valueserp.AsyncGoogleClient.search") as mock_search:
            mock_search.return_value = {'result': 'success'}
            result = await client.web_search('test')
            mock_search.assert_called_once_with(params={'q': 'test', 'location': None})
            assert isinstance(result, WebSERP)
            assert result.raw == {'result': 'success'}


    @pytest.mark.asyncio
    async def test_site_web_search_success(self, client: AsyncGoogleClient):
        with mock.patch("valueserp.AsyncGoogleClient.search") as mock_search:
            mock_search.return_value = {'result': 'success'}
            result = await client.web_search('test', site='example.com')
            mock_search.assert_called_once_with(
                params={'q': 'site:example.com test', 'location': None},
            )
            assert isinstance(result, WebSERP)
            assert result.raw == {'result': 'success'}
