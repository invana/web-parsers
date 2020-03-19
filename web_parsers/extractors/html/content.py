from web_parsers.extractors.base import ExtractorBase, ContentExtractorBase
from web_parsers.utils.selectors import extract_html_field
from web_parsers.utils.url import get_urn, get_domain, get_absolute_url
import json


class ParagraphsExtractor(ExtractorBase):
    def run(self):
        data = {}
        extracted_data = []
        elements = self.html_selector.css("p::text").extract()
        for el in elements:
            extracted_data.append(el)
        data[self.extractor_id] = [d.strip() for d in extracted_data]
        return data


class HeadingsExtractor(ExtractorBase):
    def run(self):
        data = {}
        extracted_data = []
        heading_tags = ["h1", "h2", "h3", "h4", "h5", "h6", "h7"]
        elements = self.html_selector.css("::text,".join(heading_tags)).extract()
        for el in elements:
            extracted_data.append(el)
        data[self.extractor_id] = [d.strip() for d in extracted_data if d.strip()]
        return data


class MainContentExtractor(ExtractorBase):
    # TODO - implement this
    pass


class TableContentExtractor(ExtractorBase):
    def run(self):
        data = {}
        tables = []
        for table in self.html_selector.css("table"):
            table_data = []
            table_headers = [th.extract() for th in table.css("thead tr th::text")]
            for row in table.css("tbody tr"):
                row_data = [td.extract() for td in row.css("td::text")]
                row_dict = dict(zip(table_headers, row_data))
                table_data.append(row_dict)
            tables.append(table_data)
        data[self.extractor_id] = tables
        return data


class MetaTagExtractor(ExtractorBase):
    def run(self):
        data = {}
        meta_data_dict = {}

        elements = self.html_selector.css('meta')
        for element in elements:
            # for open graph type of meta tags
            meta_property = element.xpath("@{0}".format('property')).extract_first()
            if meta_property:
                meta_property = meta_property.replace(":", "__").replace(".", "__")
                meta_data_dict[meta_property] = element.xpath(
                    "@{0}".format('content')).extract_first() or element.xpath("@{0}".format('value')).extract_first()

            meta_name = element.xpath("@{0}".format('name')).extract_first()
            if meta_name:
                meta_name = meta_name.replace(":", "__").replace(".", "__")
                meta_data_dict["meta__{}".format(meta_name)] = element.xpath(
                    "@{0}".format('content')).extract_first() or element.xpath("@{0}".format('value')).extract_first()

        try:
            title = self.html_selector.css('title::text').get()
            if title:
                meta_data_dict["title"] = title
        except Exception as e:
            pass
        data[self.extractor_id] = meta_data_dict
        return data


class CustomDataExtractor(ContentExtractorBase):
    extracted_data = {}

    def add_to_field(self, field_data=None, extractor_field=None):
        if extractor_field.flatten_data:
            if field_data is not None:
                self.extracted_data.update(field_data)
        else:
            self.extracted_data[extractor_field.field_id] = field_data

    def run(self):
        extractor_fields = self.extractor.extractor_fields
        for extractor_field in extractor_fields:
            nodes = self.html_selector.css(extractor_field.element_query.get("value"))
            child_selectors = extractor_field.child_selectors
            if extractor_field.data_type.startswith("List"):
                extracted_items = []
                if extractor_field.data_attribute == "element":
                    for node in nodes:
                        extracted_item = {}
                        for child_extractor in child_selectors:
                            extracted_item[child_extractor.field_id] = extract_html_field(
                                node, child_extractor
                            )
                        extracted_items.append(extracted_item)
                    self.add_to_field(field_data=extracted_items, extractor_field=extractor_field)
                else:
                    extracted_items = []
                    for node in nodes:
                        extracted_items.append(extract_html_field(
                            node, extractor_field
                        ))
                    self.add_to_field(field_data=extracted_items, extractor_field=extractor_field)

            else:
                if extractor_field.data_attribute == "element":
                    node = nodes[0]
                    extracted_item = {}
                    for child_extractor in child_selectors:
                        extracted_item[child_extractor.field_id] = extract_html_field(
                            node, child_extractor
                        )
                    self.add_to_field(field_data=extracted_item, extractor_field=extractor_field)

                else:
                    field_data = extract_html_field(
                        self.html_selector, extractor_field
                    )
                    self.add_to_field(field_data=field_data, extractor_field=extractor_field)

        return {self.extractor_id: self.extracted_data}

    # def run(self):
    #     data = {}
    #     extracted_data = {}
    #     for extractor_item in self.extractor.extractor_fields:
    #         if extractor_item.data_attribute == 'element' and extractor_item.child_selectors.__len__() > 0:
    #             # TODO - currently only support multiple elements strategy. what if multiple=False
    #             # review this; not sure if this is still applicable.
    #             elements = self.html_selector.css(extractor_item.element_query.get("value"))
    #             elements_data = []
    #             for el in elements:
    #                 datum = {}
    #                 for child_selector in extractor_item.child_selectors:
    #                     _d = extract_html_field(el, child_selector)
    #                     datum[child_selector.field_id] = _d if _d else None
    #                 elements_data.append(datum)
    #             data_type = extractor_item.data_type
    #             if data_type.startswith("List") is False:
    #                 single_data = elements_data[0]
    #                 extracted_data[extractor_item.field_id] = single_data
    #             else:
    #                 extracted_data[extractor_item.field_id] = elements_data
    #         else:
    #             _d = extract_html_field(self.html_selector, extractor_item)
    #             extracted_data[extractor_item.field_id] = _d
    #         if extractor_item.flatten_data is True:
    #             extracted_data[extractor_item.field_id] = self.flatten_data(extracted_data[extractor_item.field_id])
    #
    #     data[self.extractor_id] = extracted_data
    #     return data


class IconsExtractor(ExtractorBase):
    def run(self):
        data = {}
        meta_data_dict = {}

        favicon = self.html_selector.xpath('//link[@rel="shortcut icon"]').xpath("@href").get()
        if favicon:
            meta_data_dict['favicon'] = get_absolute_url(url=favicon, origin_url=self.url)

        elements = self.html_selector.xpath('//link[@rel="icon" or @rel="apple-touch-icon-precomposed"]')
        for element in elements:
            # for open graph type of meta tags
            meta_property = element.xpath("@sizes").extract_first()
            if meta_property:
                meta_property = meta_property.replace(":", "__").replace(".", "__")
                meta_data_dict[meta_property] = element.xpath("@{0}".format('href')).extract_first()
        data[self.extractor_id] = meta_data_dict
        return data


class JSONLDExtractor(ExtractorBase):

    def run(self):
        data = {}
        extracted_data = []

        elements = self.html_selector.xpath('//script[@type="application/ld+json"]/text()').extract()
        for element in elements:
            # for open graph type of meta tags
            try:
                element = element.strip()
                element = json.loads(element)
                extracted_data.append(element)
            except Exception as e:
                pass
        data[self.extractor_id] = extracted_data
        return data


class PlainHTMLContentExtractor(ExtractorBase):

    def run(self):
        return {self.extractor_id: self.html_selector.__str__()}


class FeedUrlExtractor(ExtractorBase):
    def run(self):
        data = {self.extractor_id: {}}
        data[self.extractor_id]['rss__xml'] = self.html_selector.xpath('//link[@type="application/rss+xml"]').xpath(
            "@href").extract_first()
        data[self.extractor_id]['rss__atom'] = self.html_selector.xpath('//link[@type="application/atom+xml"]').xpath(
            "@href").extract_first()
        return data


class PageOverviewExtractor(ContentExtractorBase):

    def run(self):
        data = {}

        meta_tags_data = MetaTagExtractor(
            url=self.url,
            html_selector=self.html_selector,
            extractor_id=self.extractor_id
        ).run().get(self.extractor_id, {})

        paragraphs_data = ParagraphsExtractor(
            url=self.url,
            html_selector=self.html_selector,
            extractor_id="paragraphs"
        ).run().get("paragraphs", {})
        # TODO - clean the data, that is extracted. ex:  meta_tags_data.get("title")
        extracted_data = {
            "title":
                meta_tags_data.get("title") or
                meta_tags_data.get("meta__title") or
                meta_tags_data.get("og__title") or
                meta_tags_data.get("fb__title") or
                meta_tags_data.get("meta__twitter__title"),
            "description":
                meta_tags_data.get("description") or
                meta_tags_data.get("meta__description") or
                meta_tags_data.get("og__description") or
                meta_tags_data.get("fb__description") or
                meta_tags_data.get("meta__twitter__description"),
            "image":
                meta_tags_data.get("image") or
                meta_tags_data.get("meta__image") or
                meta_tags_data.get("og__image") or
                meta_tags_data.get("fb__image") or
                meta_tags_data.get("meta__twitter__image"),
            "url":
                meta_tags_data.get("url") or
                meta_tags_data.get("meta__url") or
                meta_tags_data.get("og__url") or
                meta_tags_data.get("fb__url") or
                meta_tags_data.get("meta__twitter__url"),
            "page_type": meta_tags_data.get("og__type"),
            "keywords": meta_tags_data.get("meta__keywords"),
            "domain": get_domain(self.url),
            "first_paragraph": paragraphs_data[0] if len(paragraphs_data) > 0 else None,
            "shortlink_url": self.html_selector.xpath('//link[@rel="shortlink"]').xpath("@href").extract_first(),
            "canonical_url": self.html_selector.xpath('//link[@rel="canonical"]').xpath("@href").extract_first()
        }
        data[self.extractor_id] = extracted_data
        return data
