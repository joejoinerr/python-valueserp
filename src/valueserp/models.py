"""Provides models for SERP information and features."""

from __future__ import annotations

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


@dataclasses.dataclass
class OrganicLink:
    """Represents a standard organic search result ("blue link").

    Attributes:
        position: The position of the link amongst all organic results.
        block_position: The position of the link amongst all SERP features.
        title: The title of the link.
        url: The URL of the destination page.
        url_displayed: The URL as it is displayed in search results.
        description: The description (snippet) associated with the link.
        date: The date associated with the result, if shown.
    """

    position: int | None
    block_position: int | None = dataclasses.field(repr=False)
    title: str | None = dataclasses.field(repr=False)
    url: str | None
    url_displayed: str | None = dataclasses.field(repr=False)
    description: str | None = dataclasses.field(repr=False)
    date: str | None = dataclasses.field(repr=False)


@dataclasses.dataclass
class FeaturedSnippet:
    """Represents a featured snippet or answer box result.

    Attributes:
        text: The text within the featured snippet.
        title: The title of the featured snippet link.
        source_url: The URL from where the featured snippet is sourced.
    """

    text: str | None
    title: str | None
    source_url: str | None


@dataclasses.dataclass
class PAAItem:
    """Represents an item under the "People also ask" (PAA) accordion.

    Attributes:
        question: The question text of the PAA item.
        answer: The answer text of the PAA item.
        source_url: The URL from where the PAA item is sourced.
    """

    question: str | None
    answer: str | None
    source_url: str | None
