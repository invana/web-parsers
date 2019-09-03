from parsel import Selector
from importlib import import_module
import logging

logger = logging.getLogger(__name__)


class ExtractionEngine(object):

    def __init__(self, url=None, html=None, extraction_manifest=None):
        self.html = html
        self.url = url
        self.extraction_config = extraction_manifest

    def convert_html_to_selector(self):
        return Selector(self.html)

    def run_extractor(self, selector=None, extractor=None):
        extractor_type = extractor.get("extractor_type")
        extractor_id = extractor.get("extractor_id")
        logger.info("Running extractor:'{}' on url:{}".format(extractor_id, self.url))
        driver_klass_module = import_module(f'extraction_engine.extractors')
        driver_klass = getattr(driver_klass_module, extractor_type)
        if extractor_type is None:
            return {extractor_id: None}
        else:
            try:
                extractor_object = driver_klass(response=selector,
                                                extractor=extractor,
                                                extractor_id=extractor_id)
                data = extractor_object.run()
                return data
            except Exception as e:
                logger.error("Failed to engine the extractor_id {} on url {} with error:".format(extractor_id,
                                                                                              self.url,
                                                                                              e))
        return {extractor_id: None}

    def extract_data(self, ):
        all_extracted_data = {}
        selector = self.convert_html_to_selector()
        for extractor in self.extraction_config.get('extractors', []):
            extracted_data = self.run_extractor(selector=selector, extractor=extractor)
            all_extracted_data.update(extracted_data)
        return all_extracted_data
