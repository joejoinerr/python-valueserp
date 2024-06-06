"""Utility functions."""

from __future__ import annotations

import httpx

from valueserp import exceptions


def parse_response_error(exception: httpx.HTTPStatusError) -> None:
    """Parses a response and raises a relevant exception."""
    status_code = exception.response.status_code
    if status_code == 401:
        raise exceptions.InvalidCredentialsError() from exception
    raw_json = exception.response.json()
    message = raw_json["request_info"].get("message", "No additional information.")
    raise exceptions.ResponseError(
        status_code=status_code, response_message=message
    ) from exception
