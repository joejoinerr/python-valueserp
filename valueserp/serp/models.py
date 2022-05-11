import dataclasses
from typing import Optional


@dataclasses.dataclass
class OrganicLink:
    position: int
    block_position: int = dataclasses.field(repr=False)
    title: str = dataclasses.field(repr=False)
    url: str
    url_displayed: str = dataclasses.field(repr=False)
    description: Optional[str] = dataclasses.field(default=None, repr=False)
    date: Optional[str] = dataclasses.field(default=None, repr=False)


@dataclasses.dataclass
class FeaturedSnippet:
    text: str
    title: str
    source_url: str


@dataclasses.dataclass
class PAAItem:
    question: str
    answer: str
    source_url: str
