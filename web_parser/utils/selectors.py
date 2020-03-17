import importlib
from parsel import Selector


def convert_html_to_selector(html):
    return Selector(html)


class SelectorExtractor(object):

    @staticmethod
    def get_list_data(elements=None):
        data_cleaned = []
        data = elements.extract()
        for i, datum in enumerate(data):
            if datum:
                data_cleaned.append(datum.strip())
        return data_cleaned

    @staticmethod
    def get_single_data(elements=None):
        data = elements.extract_first()
        if data:
            return data.strip()
        return data


def transform_data(data=None, data_type=None):
    fields = importlib.import_module("web_parser.fields")
    Klass = getattr(fields, data_type)
    data = Klass(data=data).transform()
    return data


def clean_data(elements=None, items_extractor=None):
    """

    This is where are the extracted data will be cleaned up and applied functions and data types as needed.

    :param elements:
    :param items_extractor:
    :return:
    """
    data_type = items_extractor.data_type
    if data_type.startswith("List"):
        multiple = True
    else:
        multiple = False

    data_extractor = SelectorExtractor()
    if multiple is True:
        extracted_data = data_extractor.get_list_data(elements=elements)
    else:
        extracted_data = data_extractor.get_single_data(elements=elements)
    data = transform_data(data=extracted_data, data_type=data_type)
    return data


def get_elements_element(html_element, items_extractor):
    item_query = items_extractor.item_query
    if items_extractor.data_attribute in ['text']:
        if item_query.get("type") == 'css':
            elements = html_element.css("{0}::{1}".format(item_query.get('value'),
                                                          items_extractor.data_attribute))
            return clean_data(elements=elements, items_extractor=items_extractor)
        else:
            elements = html_element.xpath("{0}/{1}".format(item_query.get('value'),
                                                           items_extractor.data_attribute))
            return clean_data(elements=elements, items_extractor=items_extractor)
    elif items_extractor.data_attribute == 'html':
        if item_query.get('type') == 'css':
            elements = html_element.css(item_query.get('value'))
            return clean_data(elements=elements, items_extractor=items_extractor)
        else:
            elements = html_element.xpath("{0}/{1}".format(item_query.get('value'),
                                                           items_extractor.data_attribute))
            return clean_data(elements=elements, items_extractor=items_extractor)
    else:
        if item_query.get('type') == 'css':
            elements = html_element.css(item_query.get('value')) \
                .xpath("@{0}".format(items_extractor.data_attribute))
            return clean_data(elements=elements, items_extractor=items_extractor)
        else:
            elements = html_element.xpath("{0}/{1}".format(item_query.get('value'),
                                                           items_extractor.data_attribute))
            return clean_data(elements=elements, items_extractor=items_extractor)
