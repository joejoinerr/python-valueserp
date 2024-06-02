"""Provides the Credentials object for use in the Client."""

from __future__ import annotations

__all__ = ["Credentials"]

import requests

from valueserp.const import API_PATH, ENDPOINT
from valueserp.exceptions import InvalidCredentialsError


class Credentials:
    """Represents the credentials (API key) used to connect to VALUE SERP.

    The object offers a `validate()` method to check that credentials work
    before using them to access the API.

    Args:
        api_key: A consumer API key provided by VALUE SERP.

    Attributes:
        api_key: A consumer API key provided by VALUE SERP.
    """

    def __init__(self, api_key: str) -> None:
        """Initializes the Credentials object."""
        self.api_key = api_key

    def validate(self) -> bool:
        """Validates the provided API key.

        This works by making a request to the `account API endpoint`_ (no cost),
        and raising an error if the request is unsuccessful.

        Returns:
            True if the API key is valid.

        Raises:
            InvalidCredentialsError: The credentials are not valid.

        .. _account API endpoint: https://www.valueserp.com/docs/account-api
        """
        params = {"api_key": self.api_key}
        account_path = ENDPOINT + API_PATH["account"]
        res = requests.get(account_path, params=params)
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if res.status_code == 401:
                raise InvalidCredentialsError() from e
            raise

        return True
