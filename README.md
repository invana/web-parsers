# Web Parser

Convert HTML, XML data into JSON using YAML configurations and occasionally with pythonic functions.

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
import yaml

html = open("page.html", "r").read()
extraction_manifest_yaml = """
- extractor_type: MetaTagExtractor
  extractor_id: meta_tags
- extractor_type: HTML2JSONExtractor
  extractor_id: content
  data_selectors:
  - selector_id: title
    selector: title
    selector_type: css
    selector_attribute: text
    data_type: RawField
"""
extraction_manifest = yaml.load(extraction_manifest_yaml,  yaml.Loader)

engine = HTMLParser(html=html, extraction_manifest=extraction_manifest)
data = engine.run()
print (data)
# {'meta_tags': {'meta__viewport': 'width=device-width, initial-scale=1', 'meta__google-site-verification': 'svzjE4Ll9L_SzXgYKt2YtOz6X6lYtCO0UrPDR0ZiRcM', 'title': 'Invana Knowledge Platform'}, 'content': {'title': 'Invana Knowledge Platform'}} 

```

### XMLParser

```python
from web_parser.parsers.xml import XMLParser
import urllib.request


xml_data = urllib.request.urlopen("https://invana.io/feed.xml").read()
json_data = XMLParser(xml_data).run()

```