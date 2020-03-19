import logging
from .alpha.html import HTMLExtractorManifest
from .alpha.xml import XMLExtractorManifest

logger = logging.getLogger(__name__)


class Owner:

    def __init__(self, title=None, ownership_type="Individual", email=None, website_url=None):
        self.title = title
        self.Individual = ownership_type
        self.email = email
        self.website_url = website_url


class WebParserManifest:
    valid_versions = ("alpha",)
    valid_parser_types = ("html", "xml")
    """
    Usage


    WebParserManifest(
        title="invana.io blogs",
        domain="invana.io",
        version="alpha",
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
                 parser_type="html",
                 domain=None,
                 version="alpha",
                 test_urls=None,
                 extractors=None,
                 owner=None,
                 ):

        if version not in self.valid_versions:
            raise Exception("version can only be '{}' for now".format(",".join(self.valid_versions)))
        if parser_type not in self.valid_parser_types:
            raise Exception("parser_type can only be '{}' for now".format(",".join(self.valid_parser_types)))

        self.title = title
        self.test_urls = test_urls
        self.version = version
        self.parser_type = parser_type
        self.domain = domain
        if owner:
            self.owner = Owner(**owner)
        else:
            self.owner = owner

        manifest_cls = None
        if self.parser_type == "html":
            manifest_cls = HTMLExtractorManifest
        elif self.parser_type == "xml":
            manifest_cls = XMLExtractorManifest

        self.extractors = []

        for extractor in extractors:
            self.extractors.append(manifest_cls(**extractor))

    def to_dict(self):
        raise NotImplementedError()
