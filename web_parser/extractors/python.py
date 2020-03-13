from web_parser.extractors.base import ExtractorBase, ContentExtractorBase
import logging

logger = logging.getLogger(__name__)


class PythonHTMLExtractor(ContentExtractorBase):
    """
Usage :


extractor_type: PythonHTMLExtractor
extractor_id: python_extractor
extractor_fn: 'def extractor_fn(html_selector=None): return {"html_selector": html_selector.__str__()}'


    """

    def run(self):
        extractor_fn = self.extractor.get("extractor_fn")
        data = {}
        global_fns = {}
        exec(extractor_fn.strip(), global_fns)
        simulate_fn = global_fns['extractor_fn']
        try:
            data[self.extractor_id] = simulate_fn(html_selector=self.html_selector)
        except Exception as e:
            logger.error("Failed to run the PythonHTMLExtractor  with error {}".format(e))
            data[self.extractor_id] = None
        return data

