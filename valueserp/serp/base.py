class BaseSERP:
    """The default base SERP from which more specific types are inherited.

    Attributes:
        raw: The raw SERP data as retrieved from the API.
    """

    def __init__(self, raw):
        self.raw = raw
