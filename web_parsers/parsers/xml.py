import xmltodict as xd
import json
from web_parsers.utils.xml import get_nodes, parse_xml, get_node_text, get_node_html
import logging
from .base import ParserBase

logger = logging.getLogger(__name__)


class XMLParser(ParserBase):
    """
from web_parsers.parsers.xml import XMLParser
from web_parsers.utils.other import yaml_to_json, generate_random_id
import pprint
import urllib.request

string_data = urllib.request.urlopen("https://invana.io/feed.xml").read()

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

xml_parser = XMLParser(string_data=string_data, extractor_manifest=xml_extractor_manifest)

# usage 1
result = xml_parser.run_extractors(flatten_extractors=True)

# usage 2
result = to_dict()


    """
    selector_key = "html_selector"

    def to_dict(self):
        return json.loads(json.dumps(xd.parse(self.string_data)))

    def parse_data(self, string_data):
        """
        this function will be used to convert html/xml tree.
        :return:
        """
        return parse_xml(string_data)
