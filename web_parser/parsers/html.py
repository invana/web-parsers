from parsel import Selector
from importlib import import_module
import logging
from web_parser.utils import convert_html_to_selector

logger = logging.getLogger(__name__)


class HTMLParserEngine(object):

    def __init__(self, url=None, html=None, extraction_manifest=None):
        self.html = html
        self.url = url
        self.extraction_config = extraction_manifest

    def run_extractor(self, selector=None, extractor=None):
        extractor_type = extractor.get("extractor_type")
        extractor_id = extractor.get("extractor_id")
        logger.info("Running extractor:'{}' on url:{}".format(extractor_id, self.url))
        driver_klass_module = import_module(f'web_parser.extractors')
        driver_klass = getattr(driver_klass_module, extractor_type)
        if extractor_type is None:
            return {extractor_id: None}
        else:
            try:
                extractor_object = driver_klass(url=self.url,
                                                html_selector=selector,
                                                extractor=extractor,
                                                extractor_id=extractor_id)
                data = extractor_object.run()
                return data
            except Exception as error:
                logger.error(
                    "Failed to parsers the extractor_id {extractor_id} on url {url} with error: {error}".format(
                        extractor_id=extractor_id,
                        url=self.url,
                        error=error)
                )
        return {extractor_id: None}

    def extract_data(self, ):
        all_extracted_data = {}
        selector = convert_html_to_selector(self.html)
        for extractor in self.extraction_config:
            extracted_data = self.run_extractor(selector=selector, extractor=extractor)
            all_extracted_data.update(extracted_data)
        return all_extracted_data
