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
        if self.manifest.extractor_items:
            data = {}
            for extraction_field, field_manifest in self.manifest.extractor_items.items():
                html_selector = HTMLElementSelector(
                    self.html_tree,
                    selector_query=field_manifest.selector_query
                )
                data[extraction_field] = html_selector.extract(element_manifest=field_manifest)
            return data
        else:
            html_selector = HTMLElementSelector(
                self.html_tree,
                selector_query=self.manifest.extractor_cls.manifest.selector_query
            )
            return html_selector.extract(element_manifest=self.manifest.extractor_cls.manifest)
