"""Provides search clients for accessing the APIs.

Currently, only Google is supported by VALUE SERP.
"""

__all__ = ['GoogleClient', 'SearchType']

import enum
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Optional,
    Union
)

import requests as requests
from requests_toolbelt.sessions import BaseUrlSession

from valueserp import const
from valueserp.exceptions import APIError
from valueserp.serp.web import WebSERP

if TYPE_CHECKING:
    import valueserp


class SearchType(enum.Enum):
    """Types of searches that can be made using the API."""

    NEWS = 'news'
    IMAGES = 'images'
    VIDEOS = 'videos'
    PLACES = 'places'
    PLACE_DETAILS = 'place_details'
    SHOPPING = 'shopping'
    PRODUCT = 'product'


class GoogleClient:
    def __init__(self, credentials: 'valueserp.Credentials'):
        self.credentials = credentials
        self._session = BaseUrlSession(const.ENDPOINT)

    def search(self,
               params: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(const.API_PATH['search'],
                                 params=params)
        return response

    def web_search(self,
                   query: str,
                   location: Union[str, 'valueserp.Location', None] = None,
                   site: Optional[str] = None,
                   **kwargs) -> WebSERP:
        if site:
            query = f'site:{site} {query}'

        search_params = {
            'q': query,
            'location': location,
        }
        search_params.update(kwargs)
        response = self.search(search_params)

        return WebSERP(response)

    def _request(self,
                 path: str,
                 request_type: str = 'GET',
                 params: Optional[Dict[str, Any]] = None,
                 headers: Optional[Dict[str, str]] = None,
                 data: Optional[Dict[str, Any]] = None) -> dict:
        final_params = {
            'api_key': self.credentials.api_key,
        }
        if isinstance(params, dict):
            final_params.update(params)

        res = self._session.request(request_type,
                                    path,
                                    params=final_params,
                                    headers=headers,
                                    json=data)
        raw_json = res.json()

        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            status_code = res.status_code
            message = raw_json['request_info'].get(
                'message', 'No additional information.')
            raise APIError(
                f'VALUE SERP API responded with status {status_code}: {message}'
            ) from e

        return raw_json
