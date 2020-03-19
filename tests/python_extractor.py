from web_parsers.parsers import HTMLParser
from web_parsers.extractors import PythonExtractorManifest
from web_parsers.utils import yaml_to_json, convert_html_to_selector
import os

path = os.getcwd()
html = open("{}/tests/page.html".format(path), "r").read()
url = "http://dummy-url.com"


def test_python_extractor():
    extraction_manifest = yaml_to_json(open("{}/tests/configs/extract-python.yaml".format(path)).read())
    result = PythonExtractorManifest(url=url,
                                  html_selector=convert_html_to_selector(html),
                                  extractor=extraction_manifest,
                                  extractor_id="python_extractor"
                                  ).run()
    assert 'python_extractor' in result
    assert result['python_extractor'] is not None
    assert type(result) is dict
