from importlib import import_module
import logging
from web_parser.utils.exceptions import InvalidExtractor

logger = logging.getLogger(__name__)
extractor_classes = import_module(f'web_parser.extractors')


class ExtractorItemManifest:

    def __init__(self, item_id=None, data_type="RawField", item_query=None,
                 data_attribute=None, child_selectors=None):
        self.item_id = item_id
        self.data_type = data_type
        self.item_query = item_query
        self.data_attribute = data_attribute
        if child_selectors:
            self.child_selectors = [ExtractorItemManifest(**child_selector) for child_selector in child_selectors]
        else:
            self.child_selectors = []

    def __repr__(self):
        return "<ExtractorItemManifest data_type='{data_type}' " \
               "item_query='{item_query}' " \
               "data_attribute='{data_attribute}' " \
               ">".format(data_type=self.data_type, item_query=self.item_query,
                          data_attribute=self.data_attribute)

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "item_query": self.item_query,
            "data_type": self.data_type,
            "data_attribute": self.data_attribute
        }


class ExtractorManifest:

    def __init__(self, extractor_type=None, extractor_id=None, extractor_items=None):
        self.extractor_type = extractor_type
        try:
            extractor_cls = getattr(extractor_classes, extractor_type)
        except AttributeError as e:
            logger.error("Failed to import the extractor_type:{extractor_type} with error {error{".format(
                extractor_type=extractor_type,
                error=e
            ))
            raise InvalidExtractor({"message": "There is no {} extractor_type in the standard extractors".format(
                self.extractor_type
            )})
        self.extractor_cls = extractor_cls
        self.extractor_id = extractor_id
        if extractor_items:
            self.extractor_items = [ExtractorItemManifest(**item_manifest) for item_manifest in extractor_items]
        else:
            self.extractor_items = None

    def to_dict(self):
        return {
            "extractor_type": self.extractor_type,
            "extractor_id": self.extractor_id,
            "extractor_items": self.extractor_items,
        }

    def __repr__(self):
        return "<ExtractorManifest extractor_id=\"{extractor_id}\" " \
               "extractor_items=\"{extractor_items}\" >".format(extractor_id=self.extractor_id,
                                                                extractor_items=self.extractor_items)


class Owner:

    def __init__(self, title=None, ownership_type="Individual", email=None, website_url=None):
        self.title = title
        self.Individual = ownership_type
        self.email = email
        self.website_url = website_url


class HTMLExtractionManifest:
    valid_versions = ("beta",)

    """
    Usage
    
    
    HTMLExtractionManifest(
        title="invana.io blogs",
        domain="invana.io",
        version="beta",
        test_urls="https://invana.io/blogs",
        extractors=[],
        owner={
            "title": "Ravi Raja Merugu",
            "ownership_type": "Individual",
            "email": "rrmerugu@gmail.com",
            "website_url": "https://rrmerugu.github.io"
        }
    )
    
    
    
    """

    def __init__(self,
                 title=None,
                 domain=None,
                 version="beta",
                 test_urls=None,
                 extractors=None,
                 owner=None,
                 ):

        if version not in self.valid_versions:
            raise Exception("version can only be '{}' for now".format(",".join(self.valid_versions)))
        self.title = title
        self.test_urls = test_urls
        self.version = version
        self.domain = domain
        if owner:
            self.owner = Owner(**owner)
        else:
            self.owner = owner
        self.extractors = []

        for extractor in extractors:
            self.extractors.append(ExtractorManifest(**extractor))

    def to_dict(self):
        raise NotImplementedError()
