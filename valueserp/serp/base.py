class BaseSERP:
    """The default base SERP from which more specific types are inherited."""

    def __init__(self, raw):
        self.raw = raw
