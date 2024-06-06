"""Tests for utility functions."""

import httpx
import pytest

from valueserp import exceptions, utils


def test_parse_response_error_401():
    """Tests the `parse_response_error` function with a 401 response."""
    exception = httpx.HTTPStatusError(
        "401 Unauthorized",
        request=httpx.Request(method="GET", url="https://example.com/"),
        response=httpx.Response(status_code=401),
    )
    with pytest.raises(exceptions.InvalidCredentialsError):
        utils.parse_response_error(exception)


def test_parse_response_error_other_status():
    """Tests the `parse_response_error` function with another 4xx or 5xx status code."""
    message = "Rate limited"
    exception = httpx.HTTPStatusError(
        "429 Too Many Requests",
        request=httpx.Request(method="GET", url="https://example.com/"),
        response=httpx.Response(
            status_code=429, json={"request_info": {"message": message}}
        ),
    )
    with pytest.raises(exceptions.ResponseError) as exc_info:
        utils.parse_response_error(exception)
    assert exc_info.value.status_code == 429
    assert exc_info.value.response_message == message
