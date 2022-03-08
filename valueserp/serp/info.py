import dataclasses


@dataclasses.dataclass
class SERPInfo:
    url: str
    query: str
    query_displayed: str
    location: str
    total_results: int
