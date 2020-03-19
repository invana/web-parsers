import xmltodict as xd
import json
from web_parsers.utils.xml import get_nodes, parse_xml, get_node_text, get_node_html
import logging

logger = logging.getLogger(__name__)


class XMLParser:
    """
from web_parsers.parsers.xml import XMLParser
from web_parsers.utils.other import yaml_to_json, generate_random_id
import pprint
import urllib.request

xml_data = urllib.request.urlopen("https://invana.io/feed.xml").read()

xml_extractor_yml = \"""
- extractor_type: CustomDataExtractor
  extractor_id: channel_info
  extractor_fields:
  - field_id: channel
    element_query:
      type: xpath
      value: '/rss/channel'
    data_attribute: element
    data_type: DictField
    child_selectors:
      - field_id: title
        element_query:
          type: xpath
          value: title
        data_attribute: text
        data_type: StringField
      - field_id: description
        element_query:
          type: xpath
          value: description
        data_attribute: text
        data_type: StringField
  - field_id: pages
    element_query:
      type: xpath
      value: '/rss/channel/item'
    data_attribute: element
    data_type: ListDictField
    child_selectors:
      - field_id: title
        element_query:
          type: xpath
          value: title
        data_attribute: text
        data_type: StringField
      - field_id: description
        element_query:
          type: xpath
          value: description
        data_attribute: text
        data_type: StringField
      - field_id: link
        element_query:
          type: xpath
          value: link
        data_attribute: text
        data_type: StringField
      - field_id: guid
        element_query:
          type: xpath
          value: guid
        data_attribute: text
        data_type: StringField
      - field_id: is_perma_link
        element_query:
          type: xpath
          value: guid
        data_attribute: isPermaLink
        data_type: StringField
\"""
xml_extractor_manifest = yaml_to_json(xml_extractor_yml)

xml_parser = XMLParser(xml_data=xml_data, extractor_manifest=xml_extractor_manifest)

# usage 1
result = xml_parser.run_extractors(flatten_extractors=True)

# usage 2
result = to_dict()


    """
    parsed_xml_data = None

    def __init__(self, xml_data, url=None, extractor_manifest=None):
        self.xml_data = xml_data
        self.url = url
        self.extractor_manifest = extractor_manifest

    def to_dict(self):
        return json.loads(json.dumps(xd.parse(self.xml_data)))

    def run_extractor(self, xml_tree=None, extractor=None):
        extractor_id = extractor.extractor_id
        logger.info("Running extractor:'{}' on url:{}".format(extractor_id, self.url))
        try:
            extractor_object = extractor.extractor_cls(
                url=self.url,
                html_selector=xml_tree,
                extractor=extractor,
                extractor_id=extractor_id
            )
            return extractor_object.run()
        except Exception as error:
            logger.error(
                "Failed to extract data from  the extractor '{extractor_id}:{extractor_type}' on url "
                "'{url}' with error: '{error}'".format(
                    extractor_id=extractor_id,
                    extractor_type=extractor.extractor_type,
                    url=self.url,
                    error=error)
            )
            return {extractor_id: None}

    @staticmethod
    def flatten_extracted_data(all_extracted_data):
        all_extracted_data_new = {}
        for k, v in all_extracted_data.items():
            all_extracted_data_new.update(v)
        return all_extracted_data_new

    def run_extractors(self, flatten_extractors=False):
        xml_tree = parse_xml(self.xml_data)

        all_extracted_data = {}
        for extractor in self.extractor_manifest.extractors:
            extracted_data = self.run_extractor(extractor=extractor, xml_tree=xml_tree)
            all_extracted_data[extractor.extractor_id] = extracted_data

        if flatten_extractors is True:
            return self.flatten_extracted_data(all_extracted_data)
        return all_extracted_data
