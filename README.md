# Web Parsers

Simple, extendable HTML and XML data extraction engine using YAML configurations and some times pythonic functions.

The idea behind this library is to build standard configuration based or python based extractors
that can be used for extracting data from web data like HTML or XML. 

This library can let users write extractors for once site and reuse it with similar site and soon etc.

[![Build Status](https://travis-ci.org/invanalabs/web_parsers.svg?branch=master)](https://travis-ci.org/invanalabs/web_parsers)
[![codecov](https://codecov.io/gh/invanalabs/web_parsers/branch/master/graph/badge.svg)](https://codecov.io/gh/invanalabs/web_parsers)

## Requirements

Python 3.6+


## Installation
```bash
pip install web-parsers 

or 

pip install -e git+https://github.com/invanalabs/web-parsers.git#egg=web_parsers
```

## How to use

### HTMLParser
```python
from web_parsers import HTMLParser
from web_parsers.manifest import WebParserManifest
import urllib.request
import yaml

string_data = urllib.request.urlopen("https://invana.io").read().decode("utf-8")
extraction_manifest_yaml = """
- extractor_type: MetaTagExtractor
  extractor_id: meta_tags
- extractor_type: CustomDataExtractor
  extractor_id: content
  extractor_fields:
  - field_id: title
    element_query: 
      type: css
      value: title
    data_attribute: text
    data_type: StringField
"""
extractor_manifest = yaml.load(extraction_manifest_yaml, yaml.Loader)

manifest = WebParserManifest(
    title="invana.io blogs",
    domain="invana.io",
    version="alpha",
    test_urls="https://invana.io/blogs",
    owner={
        "title": "Ravi Raja Merugu",
        "ownership_type": "Individual",
        "email": "rrmerugu@gmail.com",
        "website_url": "https://rrmerugu.github.io"
    },
    extractors=extractor_manifest
)

engine = HTMLParser(string_data=string_data, url="http://dummy-url.com", extractor_manifest=manifest)
data = engine.run_extractors()
print(data)
{
    "content": {
        "title": "Enrich your data with information available on the Internet | Invana"
    },
    "meta_tags": {
        "meta__description": "Connect to your databases, microservices or data from internet and create Knowledge & Data APIs in near realtime",
        "meta__viewport": "width=device-width, initial-scale=1",
        "title": "Enrich your data with information available on the Internet | Invana"
    }
}

data =  engine.run_extractors(flatten_extractors=True)
print(data)
{
    "title": "Enrich your data with information available on the Internet | Invana",
    "meta__description": "Connect to your databases, microservices or data from internet and create Knowledge & Data APIs in near realtime",
    "meta__viewport": "width=device-width, initial-scale=1",
    "title": "Enrich your data with information available on the Internet | Invana"
}
```

### XMLParser

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
result = xml_parser.run_extractors(flatten_extractors=True)
pprint.pprint( result)
{'channel': {'description': 'Connect to your databases, microservices or data '
                            'from internet and create Knowledge & Data APIs in '
                            'near realtime',
             'title': 'Enrich your data with information available on the '
                      'Internet | Invana'},
 'pages': [{'description': 'Official blog of Invana',
            'guid': 'https://invana.io/blog',
            'is_perma_link': 'true',
            'link': '/blog',
            'title': 'Blog - Updates and stories | Invana'},
            ...
            ]           
}
```