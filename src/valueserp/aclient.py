"""Provides search clients for accessing the APIs.

Currently, only Google is supported by VALUE SERP.
"""

from __future__ import annotations

__all__ = ["AsyncGoogleClient", "SearchType"]

import json
from collections.abc import Mapping
from types import TracebackType
from typing import TYPE_CHECKING, Any

import httpx
from typing_extensions import Self

from valueserp import const, exceptions, utils
from valueserp.credentials import Credentials
from valueserp.searchtype import SearchType
from valueserp.serp import WebSERP

if TYPE_CHECKING:
    import valueserp


class AsyncGoogleClient:
    """The primary async interface for interacting with Google via VALUE SERP.

    Attributes:
        credentials: An initialized :class:`valueserp.Credentials` object.
    """

    def __init__(self, credentials: Credentials, **kwargs) -> None:
        """Initializes the AsyncGoogleClient.

        Args:
            credentials: An initialized :class:`valueserp.Credentials` object.
            **kwargs: Additional keyword arguments to pass to the HTTP client.
        """
        self.credentials = credentials
        transport = httpx.AsyncHTTPTransport(retries=kwargs.get("retries", 3))
        self._session = httpx.AsyncClient(
            base_url=const.ENDPOINT,
            params={"api_key": self.credentials.api_key},
            transport=transport,
            timeout=kwargs.get("timeout", 5.0),
        )

    async def search(self, params: Mapping[str, Any]) -> Mapping[str, Any]:
        """Conducts a generic search with the API and returns the response.

        Args:
            params: Parameters to send to the API with the request.

        Returns:
            The API response as a dict parsed from JSON.
        """
        response = await self._request(const.API_PATH["search"], params=params)
        return json.loads(response)

    async def web_search(
        self,
        query: str,
        location: str | valueserp.Location | None = None,
        site: str | None = None,
        **kwargs,
    ) -> WebSERP:
        """Makes a web search.

        Any `custom parameters`_ can be added as keyword arguments and will be
        passed directly to the API.

        Args:
            query: The query to search in Google.
            location: The location to use for the search in Google.
            site: Add a domain to use a site: search
            **kwargs: Custom parameters to pass to the API.

        Returns:
            A :class:`~valueserp.serp.web.WebSERP` object containing the API
            response.

        .. _custom parameters: https://www.valueserp.com/docs/search-api/searches/google/search#googleSearchParameters
        """
        if site:
            query = f"site:{site} {query}"

        search_params = {
            "q": query,
            "location": location,
        }
        # We don't want to override anything essential.
        kwargs = {k: v for k, v in kwargs.items() if k not in search_params}
        search_params.update(kwargs)
        response = await self.search(params=search_params)

        return WebSERP(response)

    async def _request(
        self,
        path: str,
        request_type: str = "GET",
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> str:
        """Makes a request to the VALUE SERP API.

        Args:
            path: The API path to request. This must start with a '/' character.
            request_type:
                The type of HTTP request to send, such as 'GET' or 'POST'.
            params: Parameters to attach to the request as query strings.
            headers: Headers to provide with the request.
            data: JSON data to send along with the request.

        Returns:
            The API response body.

        Raises:
            APIError: The API responded with an error.
        """
        try:
            res = await self._session.request(
                request_type, path, params=params, headers=headers, json=data
            )
            res.raise_for_status()
        except httpx.HTTPStatusError as e:
            utils.parse_response_error(e)
        except httpx.RequestError as e:
            raise exceptions.RequestError() from e
        else:
            return res.text

    async def close(self) -> None:
        """Closes the HTTP session."""
        await self._session.aclose()

    async def __aenter__(self) -> Self:
        """Enters the async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exits the async context manager."""
        await self.close()
