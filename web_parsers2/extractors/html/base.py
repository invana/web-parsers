from web_parsers2.utils.html import convert_string_to_html_tree


class DataExtractorBase:
    manifest = None

    def __init__(self,
                 html_tree=None,
                 html_string=None,
                 manifest=None):
        """


        :param html_string:  string html
        :param html_tree:   html tree from lxml
        :param manifest: json format
        """

        if html_tree is not None and html_string:
            raise Exception("html_tree and html_string cannot be used at the same time, this will"
                            "create unnecessary behaviour")

        if html_tree is not None:
            self.html_tree = html_tree
        if html_string:
            self.html_tree = convert_string_to_html_tree(html_string)
        if manifest:
            self.manifest = manifest

        if self.manifest is None:
            raise Exception("Invalid manifest {}".format(self.manifest))

    @staticmethod
    def convert_to_json(data=None):
        if data is None:
            return data
        elif type(data) is dict:
            json_items = {}
            for k, item in data.items():
                if type(item) is list:
                    item_data = []
                    for i in item:
                        item_data.append(i.data)
                    json_items[k] = item_data
                else:
                    json_items[k] = item.data
            return json_items
        elif type(data) is list:
            list_items = []
            for item in data:
                list_items.append(item.get_dict())
            return list_items
        else:
            return data.get_dict()

    def _extract(self):
        raise NotImplementedError()

    def extract(self, json=True):
        data = self._extract()
        if json is False:
            return data
        return self.convert_to_json(data)
