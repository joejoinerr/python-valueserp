"""Tests for the Credentials class."""

from valueserp.credentials import Credentials


def test_credentials_init():
    """Tests the initialization of credentials."""
    creds = Credentials("TESTKEY")
    assert creds.api_key == "TESTKEY"
