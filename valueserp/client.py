from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Optional
)

import requests as requests
from requests_toolbelt.sessions import BaseUrlSession

from valueserp import const
from valueserp.exceptions import APIError

if TYPE_CHECKING:
    import valueserp


class GoogleClient:
    def __init__(self, credentials: 'valueserp.Credentials'):
        self.credentials = credentials
        self._session = BaseUrlSession(const.ENDPOINT)

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
