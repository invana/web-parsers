import logging
from web_parsers.utils import convert_html_to_selector
from .base import ParserBase

logger = logging.getLogger(__name__)


class HTMLParser(ParserBase):
    """

    extractor_manifest should be a list of extractors ie., `web_parsers.extractors.
    """
    selector_key = "html_selector"

    def __init__(self, url=None, string_data=None, extractor_manifest=None):
        super().__init__(url=url, string_data=string_data, extractor_manifest=extractor_manifest)
        if self.url is None:
            raise Exception(
                "url cannot be blank, as it is used to generate absolute urls in most of the cases, you can "
                "give http://dummy-url.com as url, if you want to give a dummy url"
            )

    def parse_data(self, string_data):
        """
        this function will be used to convert string to html tree.
        :return:
        """
        return convert_html_to_selector(string_data)
