"""Exception classes.

All exceptions inherit from the `VSError` base.
"""

from __future__ import annotations


class VSError(Exception):
    """Base package exception class."""

    pass


class InvalidCredentialsError(VSError, ValueError):
    """The provided credentials are invalid."""

    def __init__(self) -> None:
        """Initializes the InvalidCredentialsError exception."""
        super().__init__("The provided API credentials are invalid.")


class APIError(VSError):
    """The VALUE SERP API responded with an error."""

    pass


class RequestError(APIError):
    """Request to the VALUE SERP API failed."""

    def __init__(self) -> None:
        """Initializes the RequestError exception."""
        super().__init__("API request failed - no response received.")


class ResponseError(APIError):
    """Response from the VALUE SERP API was not successful."""

    def __init__(self, status_code: int, response_message: str) -> None:
        """Initializes the ResponseError exception."""
        self.status_code = status_code
        self.response_message = response_message
        super().__init__(
            f"API responded with status code {self.status_code}: {self.response_message}"
        )
