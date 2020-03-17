from .base import DataExtractorBase
from web_parsers2.elements.html import HTMLElementSelector


class CustomDataExtractor(DataExtractorBase):
    def _extract(self):
        if self.manifest.extractor_items:
            data = {}
            for extraction_field, field_extractor_manifest in self.manifest.extractor_items.items():
                html_selector = HTMLElementSelector(
                    self.html_tree,
                )
                elements = html_selector.get_elements(
                    selector_type=field_extractor_manifest.selector_query.get("type"),
                    selector_value=field_extractor_manifest.selector_query.get("value"),
                )
                data[extraction_field] = html_selector.extract(elements,
                                                               element_extractor_manifest=field_extractor_manifest)
            return data
        else:
            html_selector = HTMLElementSelector(
                self.html_tree,
            )
            elements = html_selector.get_elements(
                selector_type=self.manifest.extractor_cls.manifest.selector_query.get("type"),
                selector_value=self.manifest.extractor_cls.manifest.selector_query.get("value"),
            )
            return html_selector.extract(elements, element_extractor_manifest=self.manifest.extractor_cls.manifest)
