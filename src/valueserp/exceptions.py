"""Exception classes.

All exceptions inherit from the `VSException` base.
"""

from __future__ import annotations


class VSException(Exception):
    """Base package exception class."""

    pass


class InvalidCredentials(VSException, ValueError):
    """The provided credentials are invalid."""

    pass


class APIError(VSException):
    """The VALUE SERP API responded with an error."""

    pass


class ConnectionError(VSException):
    """Failed to connect to the VALUE SERP API."""

    def __init__(self, message: str | None = None):
        super().__init__(message or "Failed to connect to the VALUE SERP API.")


class Timeout(VSException):
    """Connection to the VALUE SERP API timed out."""

    def __init__(self, message: str | None = None):
        super().__init__(message or "Connection to the VALUE SERP API timed out.")
