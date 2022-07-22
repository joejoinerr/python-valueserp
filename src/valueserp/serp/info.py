import dataclasses


@dataclasses.dataclass
class SERPInfo:
    """Information about the search results.

    Attributes:
        url: The URL of the search results page.
        query: The query that was searched.
        query_displayed: The query as it is displayed in the search results.
        location: The location that was used to conduct the search.
        total_results: The total number of results for the search.
    """

    url: str
    query: str
    query_displayed: str
    location: str
    total_results: int
