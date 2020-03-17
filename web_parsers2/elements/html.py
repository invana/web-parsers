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
        print("data====", data)
        data_transformer_cls = getattr(fields_klass_module, data_type)
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
        if attributes_manifest.__class__.__name__ == "ExtractorManifestByElement":
            data = self.extract_attributes_from_manifest(attributes=attributes_manifest.attributes)
            return ExtractedItem(_id=self.element, field_name=attributes_manifest.field_name, data=data)
        elif attributes_manifest.__class__.__name__ == "ExtractorManifestByField":
            data = self.extract_attribute_from_manifest(
                data_type=attributes_manifest.data_type,
                data_attribute=attributes_manifest.data_attribute
            )
            print("=====", data)
            return ExtractedItem(_id=self.element, field_name=attributes_manifest.field_name, data=data)


class HTMLElementSelector:

    def __init__(self, document, url=None, selector_query=None):
        self.selector_query = selector_query
        self.url = url
        self.elements = self.get_selector(document)
        print("=====self.elements", self.elements)

    def get_selector(self, document):
        if self.selector_query.get("type") == "css":
            xpath = GenericTranslator().css_to_xpath(self.selector_query.get("value"))
        else:
            xpath = self.selector_query.get("value")
        return document.xpath(xpath)

    def extract_from_element(self, element, manifest):
        return HTMLElement(element=element). \
            extract(attributes_manifest=manifest)

    def extract(self, element_manifest=None):
        """

        Usage:

        element_manifest = [
            {'attribute': 'text', 'field_name': 'text', 'data_type': 'StringField'},
            {'attribute': 'data-id', 'field_name': 'text', 'data_type': 'StringField'}
        ]

        :param element_manifest: of type ExtractorManifestByElement
        :return:
        """
        print("element_manifest", element_manifest)
        print("sele.elements", self.elements)

        if "List" in element_manifest.data_type:
            data = []
            for element in self.elements:
                item = self.extract_from_element(element, element_manifest)
                print("=====item", item.get_dict())
                data.append(item)
            return data
        else:
            # TODO - need to write exceptions if elements length is zero
            element = self.elements[0]
            item = self.extract_from_element(element, element_manifest)
            return item

