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
        search_metadata = self.raw['search_metadata']
        search_parameters = self.raw['search_parameters']
        search_info = self.raw['search_information']

        url = search_metadata['engine_url']
        query = search_parameters['q']
        query_displayed = search_info['query_displayed']
        location = search_parameters['location']
        total_results = search_info['total_results']

        return SERPInfo(url=url,
                        query=query,
                        query_displayed=query_displayed,
                        location=location,
                        total_results=total_results)

    @property
    def links(self) -> Optional[List[OrganicLink]]:
        raw_links = self.raw['organic_results']

        links = []
        for link in raw_links:
            position = link['position']
            block_position = link['block_position']
            title = link['title']
            url = link['link']
            url_displayed = link['displayed_link']
            description = link['snippet']
            date = link.get('date')
            links.append(OrganicLink(position=position,
                                     block_position=block_position,
                                     title=title,
                                     url=url,
                                     url_displayed=url_displayed,
                                     description=description,
                                     date=date))

        return links

    @property
    def featured_snippet(self) -> Optional[FeaturedSnippet]:
        raw_snippet = self.raw.get('answer_box')
        if not raw_snippet:
            return None

        featured_answer = raw_snippet['answers'][0]
        text = featured_answer['answer']
        title = featured_answer['source']['title']
        source_url = featured_answer['source']['link']
        return FeaturedSnippet(text=text,
                               title=title,
                               source_url=source_url)

    @property
    def related_searches(self) -> Optional[List[str]]:
        raw_rel_searches = self.raw.get('related_searches')
        if not raw_rel_searches:
            return None

        related_searches = set(search['query'] for search in raw_rel_searches)
        return list(related_searches)

    @property
    def people_also_ask(self) -> Optional[List[PAAItem]]:
        raw_paa = self.raw.get('related_questions')
        if not raw_paa:
            return None

        paa_items = []
        for paa in raw_paa:
            query = paa['question']
            answer = paa['answer']
            source_url = paa['source']['link']
            paa_items.append(PAAItem(question=query,
                                     answer=answer,
                                     source_url=source_url))

        return paa_items
