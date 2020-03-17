from web_parser.utils import yaml_to_json
import os
import pprint
from web_parser.parsers import HTMLParser
from web_parser.manifest import HTMLExtractionManifest

path = os.getcwd()
html = open("{}/tests/page.html".format(path), "r").read()
extraction_manifest = yaml_to_json(open("{}/tests/configs/extract_full.yaml".format(path)).read())

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

engine = HTMLParser(html_string=html, url="http://localhost", extraction_manifest=manifest)
result = engine.run()

pprint.pprint(result)
