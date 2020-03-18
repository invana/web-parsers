# Web Parser

## Introduction

Simple, extendable HTML and XML data extraction engine using YAML configurations and some times pythonic extractors.


## Requirements

Python 3.6, 3.7 and  3.8


## Simple Usage

```python

from web_parser import HTMLParser
from web_parser.manifest import HTMLExtractionManifest
import urllib.request
import yaml

html_string = urllib.request.urlopen("https://invana.io").read().decode("utf-8")
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
data = engine.run(flatten_extractors=False)
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

