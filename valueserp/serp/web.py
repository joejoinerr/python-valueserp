from __future__ import annotations

from typing import List, Optional

from valueserp.serp.base import BaseSERP
from valueserp.serp.info import SERPInfo
from valueserp.serp.models import (
    FeaturedSnippet,
    OrganicLink,
    PAAItem
)


class WebSERP(BaseSERP):
    def __init__(self, raw):
        super().__init__(raw)

    def info(self) -> SERPInfo:
        search_metadata = self.raw.get('search_metadata', {})
        search_parameters = self.raw.get('search_parameters', {})
        search_info = self.raw.get('search_information', {})

        return SERPInfo(url=search_metadata.get('engine_url'),
                        query=search_parameters.get('q'),
                        query_displayed=search_info.get('query_displayed'),
                        location=search_parameters.get('location'),
                        total_results=search_info.get('total_results'))

    @property
    def links(self) -> List[OrganicLink]:
        raw_links = self.raw.get('organic_results', [])

        links = []
        for link in raw_links:
            links.append(OrganicLink(position=link.get('position'),
                                     block_position=link.get('block_position'),
                                     title=link.get('title'),
                                     url=link.get('link'),
                                     url_displayed=link.get('displayed_link'),
                                     description=link.get('snippet'),
                                     date=link.get('date')))

        return links

    @property
    def featured_snippet(self) -> Optional[FeaturedSnippet]:
        raw_snippet = self.raw.get('answer_box')
        if not raw_snippet:
            return None

        featured_answer = raw_snippet.get('answers', [{}])[0]
        featured_answer_source = featured_answer.get('source', {})
        return FeaturedSnippet(text=featured_answer.get('answer'),
                               title=featured_answer_source.get('title'),
                               source_url=featured_answer_source.get('link'))

    @property
    def related_searches(self) -> List[str] | None:
        raw_rel_searches = self.raw.get('related_searches', [])
        if not raw_rel_searches:
            return None

        related_searches = set(query for search in raw_rel_searches
                               if (query := search.get('query')))
        return list(related_searches)

    @property
    def people_also_ask(self) -> Optional[List[PAAItem]]:
        raw_paa = self.raw.get('related_questions', [])
        if not raw_paa:
            return None

        paa_items = []
        for paa in raw_paa:
            source_url = paa.get('source', {}).get('link')
            paa_items.append(PAAItem(question=paa.get('question'),
                                     answer=paa.get('answer'),
                                     source_url=source_url))

        return paa_items
