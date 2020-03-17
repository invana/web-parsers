from web_parsers2.utils.html import convert_string_to_html_tree


class HTMLExtractionManager:

    def __init__(self, html_string=None, html_tree=None, url=None, generate_absolute_urls=True,
                 extraction_manifest=None):
        if html_tree and html_string:
            raise Exception("html_tree and html_string cannot be used at the same time, this will"
                            "create unnecessary behaviour")
        if generate_absolute_urls is True and url is None:
            raise Exception("when generate_absolute_urls=True, provide the url from which content is"
                            " extracted, so that, we can create absolute urls")
        elif generate_absolute_urls is False and url is not None:
            raise Exception("when generate_absolute_urls=False, url will not be used to create absolute urls")

        if html_tree:
            self.html_tree = html_tree
        if html_string:
            self.html_tree = convert_string_to_html_tree(html_string)
        self.url = url
        self.extraction_manifest = extraction_manifest

    def run_extractor(self, single_extractor_manifest=None, return_json=None):
        return single_extractor_manifest.extractor_cls(
            html_tree=self.html_tree,
            manifest=single_extractor_manifest
        ).extract(json=return_json)

    def run_extractors(self, return_json=True):
        data = {}
        for single_extractor_manifest in self.extraction_manifest.extractors:
            data[single_extractor_manifest.extractor_id] = self.run_extractor(
                single_extractor_manifest=single_extractor_manifest,
                return_json=return_json
            )
        return data
