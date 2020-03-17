from lxml import etree
from web_parser.items import ExtractedItem
from importlib import import_module
from cssselect import GenericTranslator, SelectorError, HTMLTranslator

fields_klass_module = import_module(f'web_parser.fields')


class HTMLElement:

    def __init__(self, url=None, element=None):
        """

        :param element:
        :param url:
        """
        self.element = element
        self.url = url

    def get_all_attributes(self, get_html=True, get_text=True):
        """
        This will return all the attributes of an element like id, data-id etc along with html and text data
        :return:
        """
        all_attributes = self.element.attrib
        if get_html is True:
            all_attributes['html'] = etree.tostring(self.element, pretty_print=False)
        if get_text is True:
            all_attributes['text'] = ''.join(self.element.itertext()).strip()
        return all_attributes

    @staticmethod
    def transform_attribute_data_type(data_type=None, data=None):
        data_transformer_cls = getattr(fields_klass_module, data_type.lstrip("List"))
        return data_transformer_cls(data).transform()

    def extract_attribute(self, attribute=None):
        if attribute == "text":
            data = ''.join(self.element.itertext()).strip()
        elif attribute == "html":
            data = etree.tostring(self.element, pretty_print=False)
        else:
            data = self.element.get(attribute)
        return data

    def extract_attribute_from_manifest(self, data_attribute=None, data_type=None, ):
        """

        :param data_attribute: class, id, data-id etc
        :param data_type: StringField etc
        :return:
        """
        data = self.extract_attribute(data_attribute)
        return self.transform_attribute_data_type(
            data_type=data_type,
            data=data)

    def extract_attributes_from_manifest(self, attributes=None):
        """

        Usage:
        attributes = [
            {'attribute': 'text', 'field_name': 'text', 'data_type': 'StringField'},
            {'attribute': 'data-id', 'field_name': 'text', 'data_type': 'StringField'}
        ]

        :param attributes:
        :return:
        """
        data = {}
        for attribute_manifest in attributes:
            data[attribute_manifest['field_name']] = self.extract_attribute_from_manifest(
                data_type=attribute_manifest['data_type'],
                data_attribute=attribute_manifest['attribute']
            )
        return data

    def extract(self, attributes_manifest=None):
        """

        :param attributes_manifest: list of extractor
        :return:
        """
        data = None
        if attributes_manifest.__class__.__name__ == "ExtractorManifestByElement":
            data = self.extract_attributes_from_manifest(attributes=attributes_manifest.attributes)
        elif attributes_manifest.__class__.__name__ == "ExtractorManifestByField":
            data = self.extract_attribute_from_manifest(
                data_type=attributes_manifest.data_type,
                data_attribute=attributes_manifest.data_attribute
            )
        return ExtractedItem(_id=self.element, field_name=attributes_manifest.field_name, data=data)


class HTMLElementSelector:
    """

    Usage:

        from web_parsers2.manifest.v1 import ExtractorManifestByField

        selector_query = {"type":"css", "value": "h1"}
        element_extractor_manifest = ExtractorManifestByField( **{ 'data_type':'ListStringField',
        'selector_query':{'type': 'css', 'value': 'a'},
        'data_attribute':'href' }>

        html_selector = HTMLElementSelector(
            self.html_tree,
        )
        elements = html_selector.get_elements(
            selector_type=selector_query.get("type"),
            selector_value=selector_query.get("value"),
        )
        return html_selector.extract(elements, element_extractor_manifest=element_extractor_manifest)


    """

    def __init__(self, html_tree, url=None):
        self.html_tree = html_tree
        self.url = url

    def get_element_by_css(self, css):
        xpath = GenericTranslator().css_to_xpath(css)
        return self.html_tree.xpath(xpath)

    def get_element_by_xpath(self, xpath):
        return self.html_tree.xpath(xpath)

    def get_elements(self, selector_type="css", selector_value=None):
        if selector_type == "css":
            elements = self.get_element_by_css(selector_value)
        else:
            elements = self.get_element_by_xpath(selector_value)
        return [HTMLElement(element=element) for element in elements]

    def extract(self, elements,
                # data_type=None, selector_query=None, data_attribute=None, attributes=None
                element_extractor_manifest=None):
        """

        Usage:

        element_extractor_manifest =  <ExtractorManifestByField data_type='ListStringField'
        selector_query='{'type': 'css', 'value': 'a'}' data_attribute='href' >

        :param element_extractor_manifest: of type ExtractorManifestByElement
        :param elements: html elements
        :return:
        """
        if "List" in element_extractor_manifest.data_type:
            data = []
            for element in elements:
                item = element.extract(attributes_manifest=element_extractor_manifest)
                data.append(item)
            return data
        else:
            if elements and elements.__len__() > 0:
                element = elements[0]
                item = element.extract(attributes_manifest=element_extractor_manifest)
                return item
            else:
                return None
