# Extraction Engine

Convert HTML data into cleaned JSON  using YAML configurations



[![Build Status](https://travis-ci.org/invanalabs/web-parser.svg?branch=master)](https://travis-ci.org/invanalabs/web-parser)
[![codecov](https://codecov.io/gh/invanalabs/web-parser/branch/master/graph/badge.svg)](https://codecov.io/gh/invanalabs/web-parser)

## How to install
```bash
pip install -e git+https://github.com/invanalabs/web-parser.git#egg=web_parser
```

## How to use

```python


from web_parser import HTMLParserEngine
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

engine = HTMLParserEngine(html=html, extraction_manifest=extraction_manifest)
data = engine.extract_data()
print (data)
# {'meta_tags': {'meta__viewport': 'width=device-width, initial-scale=1', 'meta__google-site-verification': 'svzjE4Ll9L_SzXgYKt2YtOz6X6lYtCO0UrPDR0ZiRcM', 'title': 'Invana Knowledge Platform'}, 'content': {'title': 'Invana Knowledge Platform'}} 

```
