"""Exception classes.

All exceptions inherit from the `VSException` base.
"""


class VSException(Exception):
    """Base library exception."""
    pass


class InvalidCredentials(VSException, ValueError):
    """Provided credentials are not valid."""
    pass


class APIError(VSException):
    """The VALUE SERP API returned an error."""
    pass
