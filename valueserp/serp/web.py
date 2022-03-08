from valueserp.serp.base import BaseSERP


class WebSERP(BaseSERP):
    def __init__(self, raw):
        super().__init__(raw)

    @property
    def info(self) -> SERPInfo:
        url = self.raw.get('url') or None
        title = self.raw.get('title') or None
        html = self.raw.get('html') or None
        text = self.raw.get('text') or None
        status = self.raw.get('status') or None
        user_agent = self.raw.get('useragent') or None

        return SERPInfo(url=url,
                        title=title,
                        html=html,
                        text=text,
                        status=status,
                        user_agent=user_agent)

    @property
    def links(self) -> Union[List[BlueLink], None]:
        try:
            raw_links = self.raw['links']
        except KeyError:
            return None

        links = []
        for i, item in enumerate(raw_links, 1):
            position = i
            title = item.get('title') or None
            url = item.get('href') or None
            description = item.get('description') or None
            links.append(BlueLink(position=position,
                                  title=title,
                                  url=url,
                                  description=description))

        return links

    @property
    def features(self) -> Union[Set[str], None]:
        try:
            raw_features = self.raw['features']
        except KeyError:
            return None

        return set(raw_features)

    @property
    def featured_snippet(self) -> Union[FeaturedSnippet, None]:
        try:
            raw_snippet = self.raw.get('answboxlink', [])[0]
        except IndexError:
            return None

        text = raw_snippet.get('text') or None
        title = raw_snippet.get('title') or None
        url = raw_snippet.get('href') or None

        return FeaturedSnippet(text=text, title=title, url=url)

    @property
    def related_searches(self) -> Union[Set[str], None]:
        try:
            raw_related = self.raw['relatedsearches']
        except KeyError:
            return None

        related = []
        for item in raw_related:
            query = item.get('query')
            if query:
                related.append(query)

        return set(related)

    @property
    def people_also_search(self) -> Union[Set[str], None]:
        raw_pas = self.raw.get('peoplesearchfor', [])
        if not raw_pas:
            return None

        pas = []
        for item in raw_pas:
            query = item.get('query')
            if query and query.strip().lower() != 'people also search for':
                pas.append(query)

        return set(pas)

    @property
    def knowledge_base(self) -> Union[List[KnowledgeBaseItem], None]:
        raw_kb = self.raw.get('knowledgebaseitems', [])
        if not raw_kb:
            return None

        kb_items = []
        for item in raw_kb:
            type_ = item.get('kbtype') or None
            id_ = int(item.get('kbnumber')) or None
            content = item.get('content') or None
            schema = item.get('kbschema') or None
            kb_items.append(KnowledgeBaseItem(type=type_,
                                              id=id_,
                                              content=content,
                                              schema=schema))

        return kb_items

    @property
    def people_also_ask(self) -> Union[List[PAAQuestion], None]:
        raw_paa = self.raw.get('peoplealsoask', [])
        if not raw_paa:
            return None

        paa_items = []
        for item in raw_paa:
            query = item.get('query') or None
            title = item.get('title') or None
            description = item.get('description') or None
            url = item.get('href') or None
            paa_items.append(PAAQuestion(query=query,
                                         title=title,
                                         description=description,
                                         url=url))

        return paa_items
