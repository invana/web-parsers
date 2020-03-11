"""


"""


class ExtractorBase:
    """

    """

    def __init__(self, html_selector=None, extractor=None, extractor_id=None, extractor_fn=None):
        """
        :param html_selector: html html_selector of the request
        :param extractor: extractor configuration in json; this is optional in most cases.
        :param extractor_fn: extractor python lambda; this is optional in most cases.
        :param extractor_id: the field with which data is stored in database.
        """
        if None in [html_selector, extractor_id]:
            raise Exception(
                "Invalid input to the extractor class, html_selector, extractor and extractor_id are mandatory")
        self.html_selector = html_selector
        self.extractor = extractor
        self.extractor_id = extractor_id
        self.extractor_fn = extractor_fn
