from importlib import import_module
from lxml import etree
from web_parser.items import ExtractedItem

fields_klass_module = import_module(f'web_parser.fields')


class HTMLElement:

    def __init__(self, url=None, element=None):
        """

        # :param data_type: IntField, FloatField, StringField
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
    def transform_attribute_data_type(attribute_manifest=None, data=None):
        data_transformer_cls = getattr(fields_klass_module, attribute_manifest['data_type'])
        return data_transformer_cls(data).transform()

    def extract_attribute(self, attribute=None):
        if attribute == "text":
            data = ''.join(self.element.itertext()).strip()
        elif attribute == "html":
            data = etree.tostring(self.element, pretty_print=False)
        else:
            data = self.element.get(attribute)
        return data

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
            attribute_data = self.extract_attribute(attribute_manifest['attribute'])
            data[attribute_manifest['field_name']] = self.transform_attribute_data_type(
                attribute_manifest=attribute_manifest,
                data=attribute_data)
        return data

    def extract(self, attributes_manifest=None):
        """

        :param attributes_manifest: list of extractor
        :return:
        """
        attributes = self.extract_attributes_from_manifest(attributes=attributes_manifest.attributes)
        return ExtractedItem(_id=self.element, field_name=attributes_manifest.field_name, attributes=attributes)
