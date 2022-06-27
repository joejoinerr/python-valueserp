from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class OrganicLink:
    position: int | None
    block_position: int | None = dataclasses.field(repr=False)
    title: str | None = dataclasses.field(repr=False)
    url: str | None
    url_displayed: str | None = dataclasses.field(repr=False)
    description: str | None = dataclasses.field(repr=False)
    date: str | None = dataclasses.field(repr=False)


@dataclasses.dataclass
class FeaturedSnippet:
    text: str | None
    title: str | None
    source_url: str | None


@dataclasses.dataclass
class PAAItem:
    question: str | None
    answer: str | None
    source_url: str | None
