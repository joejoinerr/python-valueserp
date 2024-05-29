from unittest import mock

from valueserp.credentials import Credentials


def test_credentials_init():
    with mock.patch('valueserp.credentials.Credentials.validate') as mock_validate:
        mock_validate.return_value = True
        creds = Credentials("TESTKEY")
        assert creds.api_key == "TESTKEY"
        mock_validate.assert_called_once()


def test_credentials_init_no_validate():
    with mock.patch('valueserp.credentials.Credentials.validate') as mock_validate:
        mock_validate.return_value = True
        creds = Credentials("TESTKEY", auto_validate=False)
        assert creds.api_key == "TESTKEY"
        mock_validate.assert_not_called()
