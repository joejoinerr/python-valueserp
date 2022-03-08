import requests

from valueserp.const import API_PATH, ENDPOINT
from valueserp.exceptions import InvalidCredentials


class Credentials:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.validate()

    def validate(self) -> bool:
        params = {'api_key': self.api_key}
        account_path = ENDPOINT + API_PATH['account']
        res = requests.get(account_path, params=params)
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if res.status_code == 401:
                raise InvalidCredentials(
                    'The API key provided is invalid.'
                ) from e
            else:
                raise

        return True
