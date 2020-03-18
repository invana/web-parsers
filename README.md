# Web Parser

Simple, extendable HTML and XML data extraction engine using YAML configurations and some times pythonic functions.

The idea behind this library is to build standard configuration based or python based extractors
that can be used for extracting data from web data like HTML or XML. 

This library can let users write extractors for once site and reuse it with similar site and soon etc.

[![Build Status](https://travis-ci.org/invanalabs/web-parser.svg?branch=master)](https://travis-ci.org/invanalabs/web-parser)
[![codecov](https://codecov.io/gh/invanalabs/web-parser/branch/master/graph/badge.svg)](https://codecov.io/gh/invanalabs/web-parser)

## Requirements

Python 3.6+


## Installation
```bash
pip install -e git+https://github.com/invanalabs/web-parser.git#egg=web_parser
```

## How to use

### HTMLParser
```python
from web_parser import HTMLParser
from web_parser.manifest import HTMLExtractionManifest
import urllib.request
import yaml

html_string = urllib.request.urlopen("https://invana.io").read().decode("utf-8")
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
extraction_manifest = yaml.load(extraction_manifest_yaml, yaml.Loader)

manifest = HTMLExtractionManifest(
    title="invana.io blogs",
    domain="invana.io",
    version="beta",
    test_urls="https://invana.io/blogs",
    owner={
        "title": "Ravi Raja Merugu",
        "ownership_type": "Individual",
        "email": "rrmerugu@gmail.com",
        "website_url": "https://rrmerugu.github.io"
    },
    extractors=extraction_manifest
)

engine = HTMLParser(html_string=html_string, url="http://dummy-url.com", extraction_manifest=manifest)
data = engine.run()
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

data = engine.run(flatten_extractors=True)
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
from web_parser.parsers.xml import XMLParser
import urllib.request


xml_data = urllib.request.urlopen("https://invana.io/feed.xml").read()
json_data = XMLParser(xml_data).run()

```