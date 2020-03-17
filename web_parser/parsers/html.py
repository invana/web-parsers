from importlib import import_module
import logging
from web_parser.utils import convert_html_to_selector
from web_parser.utils.exceptions import InvalidExtractor

logger = logging.getLogger(__name__)


class HTMLParser:
    """

    extraction_manifest should be a list of extractors ie., `web_parser.extractors.
    """

    def __init__(self, url=None, html_string=None, extraction_manifest=None):
        self.html_string = html_string
        self.url = url
        if self.url is None:
            raise Exception(
                "url cannot be blank, as it is used to generate absolute urls in most of the cases, you can "
                "give http://dummy-url.com as url, if you want to give a dummy url"
            )
        self.extraction_manifest = extraction_manifest

    def run_extractor(self, selector=None, extractor=None):

        extractor_id = extractor.extractor_id
        logger.info("Running extractor:'{}' on url:{}".format(extractor_id, self.url))
        try:
            extractor_object = extractor.extractor_cls(
                url=self.url,
                html_selector=selector,
                extractor=extractor,
                extractor_id=extractor_id
            )
            return extractor_object.run()
        except Exception as error:
            logger.error(
                "Failed to extract data from  the extractor '{extractor_id}:{extractor_type}' on url "
                "'{url}' with error: '{error}'".format(
                    extractor_id=extractor_id,
                    extractor_type=extractor.extractor_type,
                    url=self.url,
                    error=error)
            )
            return {extractor_id: None}

    @staticmethod
    def flatten_extracted_data(all_extracted_data):
        all_extracted_data_new = {}
        for k, v in all_extracted_data.items():
            all_extracted_data_new.update(v)
        return all_extracted_data_new

    def run(self, flatten_extractors=False):
        all_extracted_data = {}
        selector = convert_html_to_selector(self.html_string)
        for extractor in self.extraction_manifest.extractors:
            extracted_data = self.run_extractor(selector=selector, extractor=extractor)
            all_extracted_data.update(extracted_data)
        if flatten_extractors is True:
            return self.flatten_extracted_data(all_extracted_data)
        return all_extracted_data
