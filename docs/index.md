# Web Parsers

## Introduction

Simple, extendable HTML and XML data extraction engine using YAML configurations and some times pythonic extractors.


## Requirements

Python 3.6, 3.7 and  3.8


## Simple Usage

```python

from web_parsers import HTMLParser
from web_parsers.manifest import WebParserManifest
import urllib.request
import yaml

string_data = urllib.request.urlopen("https://invana.io").read().decode("utf-8")
extraction_manifest_yaml = """
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
    extractors=extraction_manifest
)

engine = HTMLParser(string_data=string_data, url="http://dummy-url.com", extractor_manifest=manifest)
data =  engine.run_extractors(flatten_extractors=False)
print(data)
```

## License

Copyright 2020 Invana Technology Solutions Pvt Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

