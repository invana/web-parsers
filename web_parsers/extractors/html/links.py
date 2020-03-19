from web_parsers.extractors.base import ExtractorBase, ContentExtractorBase
from web_parsers.utils.url import get_urn, get_domain


class AllLinksExtractor(ExtractorBase):
    def run(self):
        data = {}
        extracted_data = []
        links = self.html_selector.css("a").xpath("@href").extract()

        for link in links:
            if link and not link.startswith("#"):
                extracted_data.append(link)
        data[self.extractor_id] = extracted_data
        return data


class AllLinksAnalyticsExtractor(ContentExtractorBase):

    def run(self):
        data = {}
        extracted_data = AllLinksExtractor(
            url=self.url,
            html_selector=self.html_selector,
            extractor=self.extractor,
            extractor_id="all_links"
        ).run().get("all_links", {})

        links_data = {}
        for link in extracted_data:
            domain = get_domain(link)
            if domain in links_data.keys():
                links_data[domain].append(link)
            else:
                links_data[domain] = [link]

        data[self.extractor_id] = [{"domain": domain, "links": domain_links, "links_count": domain_links.__len__()} for
                                   domain, domain_links in links_data.items()]

        return data


class SameDomainLinkExtractor(ExtractorBase):
    pass


class ForeignDomainLinkExtractor(ExtractorBase):
    pass


class CustomLinkExtractor(ExtractorBase):
    pass
