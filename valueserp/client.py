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
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_toolbelt.sessions import BaseUrlSession

from valueserp import const
import valueserp.exceptions
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


class TimeoutHTTPAdapter(HTTPAdapter):
    """Custom HTTPAdapter to enable a default timeout"""
    DEFAULT_TIMEOUT = 5  # seconds

    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.pop('timeout', self.DEFAULT_TIMEOUT)
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        return super().send(request, **kwargs)


class GoogleClient:
    def __init__(self, credentials: 'valueserp.Credentials'):
        self.credentials = credentials
        self._session = BaseUrlSession(const.ENDPOINT)
        # Set up default timeout and retry strategies
        retry_strategy = Retry(total=3,
                               status_forcelist=[429, 500, 502, 503, 504],
                               allowed_methods=['HEAD', 'GET', 'OPTIONS'])
        adapter = TimeoutHTTPAdapter(max_retries=retry_strategy)
        self._session.mount('https://', adapter)
        self._session.mount('http://', adapter)

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

        try:
            res = self._session.request(request_type,
                                        path,
                                        params=final_params,
                                        headers=headers,
                                        json=data)
            raw_json = res.json()
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            status_code = res.status_code
            message = raw_json['request_info'].get(
                'message', 'No additional information.')
            raise valueserp.exceptions.APIError(
                f'VALUE SERP API responded with status {status_code}: {message}'
            ) from e
        except requests.exceptions.ConnectionError as e:
            raise valueserp.exceptions.ConnectionError() from e
        except requests.exceptions.Timeout as e:
            raise valueserp.exceptions.Timeout() from e
        except requests.exceptions.RequestException as e:
            raise valueserp.exceptions.VSException(
                'An unknown error occurred.') from e

        return raw_json
