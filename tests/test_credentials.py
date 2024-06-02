from unittest import mock

from valueserp.credentials import Credentials


def test_credentials_init():
    creds = Credentials("TESTKEY")
    assert creds.api_key == "TESTKEY"
