from web_parsers.extractors.base import ExtractorBase


class ImagesExtractor(ExtractorBase):
    def run(self):
        data = {}
        images_data = []
        images_selector = self.html_selector.xpath('//img/@src').extract()
        for selector in images_selector:
            images_data.append(selector)
        data[self.extractor_id] = images_data
        return data
