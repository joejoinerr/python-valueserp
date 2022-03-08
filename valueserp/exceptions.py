class VSException(Exception):
    pass


class InvalidCredentials(VSException, ValueError):
    pass


class APIError(VSException):
    pass
