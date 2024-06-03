"""Utility functions."""

from __future__ import annotations

import httpx

from valueserp import exceptions


def parse_response_error(exception: httpx.HTTPStatusError) -> None:
    """Parses the response body and raises a ResponseError."""
    status_code = exception.response.status_code
    raw_json = exception.response.json()
    message = raw_json["request_info"].get("message", "No additional information.")
    raise exceptions.ResponseError(
        status_code=status_code, response_message=message
    ) from exception
