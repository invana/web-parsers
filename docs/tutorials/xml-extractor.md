# XML Extractor


```python

from web_parsers.manifest import WebParserManifest
from web_parsers.parsers.xml import XMLParser
from web_parsers.utils.other import yaml_to_json, generate_random_id
import pprint
import urllib.request

string_data = urllib.request.urlopen("https://invana.io/feed.xml").read()

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
manifest = WebParserManifest(
    title="invana.io blogs",
    domain="invana.io",
    version="alpha",
    test_urls=["https://invana.io/feed.xml", ],
    parser_type="xml",
    owner={
        "title": "Ravi Raja Merugu",
        "ownership_type": "Individual",
        "email": "rrmerugu@gmail.com",
        "website_url": "https://rrmerugu.github.io"
    },
    extractors=xml_extractor_manifest
)

xml_parser = XMLParser(string_data=string_data, extractor_manifest=manifest)
result = xml_parser.run_extractors(flatten_extractors=False)
pprint.pprint( result)

{'channel_info': {'channel': {
    'description': 'Connect to your databases, microservices or data '
                            'from internet and create Knowledge & Data APIs in '
                            'near realtime',
             'title': 'Enrich your data with information available on the '
                      'Internet | Invana'},
    'pages': [
        {'description': 'Official blog of Invana',
            'guid': 'https://invana.io/blog',
            'is_perma_link': 'true',
            'link': '/blog',
            'title': 'Blog - Updates and stories | Invana'
        },
            ...
            ]           
}
}
```



## Flatten Extracted data

```python
# look at the above example for a practical example with code.
xml_parser = XMLParser(string_data=string_data, extractor_manifest=manifest)
result = xml_parser.run_extractors(flatten_extractors=True)


{'channel': {
    'description': 'Connect to your databases, microservices or data '
                            'from internet and create Knowledge & Data APIs in '
                            'near realtime',
     'title': 'Enrich your data with information available on the '
                      'Internet | Invana'},
    'pages': [
        {'description': 'Official blog of Invana',
            'guid': 'https://invana.io/blog',
            'is_perma_link': 'true',
            'link': '/blog',
            'title': 'Blog - Updates and stories | Invana'
        },
            ...
            ]           
}
```