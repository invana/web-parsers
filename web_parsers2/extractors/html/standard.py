from .base import DataExtractorBase


class ParagraphExtractor(DataExtractorBase):
    manifest = {
        "data_type": "ListStringField",
        "selector_query": {
            "type": "css",
            "value": "p"
        },
        "data_attribute": "text"
    }
