from web_parser.extractors.base import ExtractorBase


class PythonBasedExtractor(ExtractorBase):
    """


    def extractor_fn(html_selector=html_selector):
        html_content = html_selector.title

        return {"data": {}, "d__d": []}


    """

    def run(self):
        extractor_fn = self.extractor.get("extractor_fn")
        data = {}
        if extractor_fn:
            data[self.extractor_id] = extractor_fn(html_selector=self.html_selector)
        return data
