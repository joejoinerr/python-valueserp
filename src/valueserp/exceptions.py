"""Exception classes.

All exceptions inherit from the `VSError` base.
"""

from __future__ import annotations


class VSError(Exception):
    """Base package exception class."""

    pass


class InvalidCredentialsError(VSError, ValueError):
    """The provided credentials are invalid."""

    pass


class APIError(VSError):
    """The VALUE SERP API responded with an error."""

    pass


class RequestConnectionError(VSError):
    """Failed to connect to the VALUE SERP API."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes the RequestConnectionError exception."""
        super().__init__(message or "Failed to connect to the VALUE SERP API.")


class RequestTimeoutError(VSError):
    """Connection to the VALUE SERP API timed out."""

    def __init__(self, message: str | None = None) -> None:
        """Initializes the RequestTimeoutError exception."""
        super().__init__(message or "Connection to the VALUE SERP API timed out.")
