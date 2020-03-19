from web_parsers.parsers.xml import XMLParser
import os
import urllib.request
from web_parsers.utils.other import yaml_to_json, generate_random_id

path = os.getcwd()


def test_xml_to_json():
    xml_data = open("{}/tests/xml/feed.xml".format(path)).read()
    json_data = XMLParser(xml_data).to_dict()
    assert type(json_data) is dict
    assert "rss" in json_data


def test_xml_extractor_with_manifest():
    xml_data = open("{}/tests/xml/feed.xml".format(path)).read().encode("utf-8")

    xml_extractor_yml = """
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


    """
    xml_extractor_manifest = yaml_to_json(xml_extractor_yml)

    xml_parser = XMLParser(xml_data=xml_data, extractor_manifest=xml_extractor_manifest)
    result = xml_parser.run_extractors()
    assert type(result) is dict
    assert "channel_info" in result
    result = xml_parser.run_extractors(flatten_extractors=True)
    assert "channel" in result
    assert "pages" in result
    assert result['channel'] is not None
