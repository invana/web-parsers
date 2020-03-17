from .custom import CustomDataExtractor
from .base import DataExtractorBase
from web_parsers2.elements.html import HTMLElementSelector


class ParagraphExtractor(CustomDataExtractor):
    manifest = {
        "data_type": "ListStringField",
        "selector_query": {
            "type": "css",
            "value": "p"
        },
        "data_attribute": "text"
    }


class HeadingsExtractor(CustomDataExtractor):
    manifest = {
        "data_type": "ListStringField",
        "selector_query": {
            "type": "css",
            "value": "h1,h2,h3,h4,h5,h6"
        },
        "data_attribute": "text"
    }


class ImagesExtractor(CustomDataExtractor):
    manifest = {
        "data_type": "ListStringField",
        "selector_query": {
            "type": "css",
            "value": "img"
        },
        "data_attribute": "src"
    }


class LinksExtractor(CustomDataExtractor):
    manifest = {
        "data_type": "ListStringField",
        "selector_query": {
            "type": "css",
            "value": "a"
        },
        "data_attribute": "href"
    }


class TableExtractor(DataExtractorBase):

    def _extract(self):

        html_selector = HTMLElementSelector(
            self.html_tree,
        )
        elements = html_selector.get_elements(
            selector_type="css",
            selector_value="table",
        )
        print("elements", elements)

        data = {}
        tables = []
        for table_element in elements:
            print("table_element", table_element)
            # table_data = []
            # table_headers = [th.extract() for th in table_element.css("thead tr th::text")]
            # for row in table_element.css("tbody tr"):
            #     row_data = [td.extract() for td in row.css("td::text")]
            #     row_dict = dict(zip(table_headers, row_data))
            #     table_data.append(row_dict)
            # tables.append(table_data)
        data[self.extractor_id] = tables
        return data
