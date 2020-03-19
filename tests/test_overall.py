from web_parser.parsers import HTMLParser
from web_parser.utils import yaml_to_json
import os
from web_parser.manifest import WebParserManifest
import pytest

path = os.getcwd()


def test_overall_web_parser_engine():
    html = open("{}/tests/page.html".format(path), "r").read()
    extraction_manifest = yaml_to_json(open("{}/tests/configs/extract.yaml".format(path)).read())
    manifest = WebParserManifest(extractors=extraction_manifest)
    engine = HTMLParser(html_string=html, url="http://localhost", extraction_manifest=manifest)
    result = engine.run()
    assert result['meta_tags'] is not None
    assert result['content'] is not None
    assert type(result) is dict
    assert "content" in result
    assert "meta_tags" in result


def test_overall_web_parser_engine_with_dictionaries():
    extraction_manifest = yaml_to_json(open("{}/tests/configs/extract_full.yaml".format(path)).read())
    html = open("{}/tests/page.html".format(path), "r").read()

    manifest = WebParserManifest(
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
    assert result['meta_tags'] is not None
    assert result['content'] is not None
    assert type(result) is dict
    assert "content" in result
    assert "meta_tags" in result
    assert result['content']['form_fields'].__len__() > 0
    assert result['content']['form_fields'][0]['input_id'] == 'name'


def test_overall_web_parser_engine_failure_case():
    html = open("{}/tests/page.html".format(path), "r").read()
    extraction_manifest = yaml_to_json(open("{}/tests/configs/extract-failcase.yaml".format(path)).read())
    manifest = WebParserManifest(extractors=extraction_manifest)
    engine = HTMLParser(html_string=html, url="http://localhost", extraction_manifest=manifest)
    result = engine.run()
    assert "meta_tags" not in result
    assert result['content'] is not None
    assert type(result) is dict


def test_overall_web_parser_engine_failure_invalid_extractor_type():
    html = open("{}/tests/page.html".format(path), "r").read()
    extraction_manifest = yaml_to_json(open("{}/tests/configs/extract-failcase2.yaml".format(path)).read())
    manifest = WebParserManifest(extractors=extraction_manifest)
    engine = HTMLParser(html_string=html, url="http://localhost", extraction_manifest=manifest)

    result = engine.run()
    assert "meta_tags" in result
    assert result['meta_tags'] is None
    assert result['content'] is not None

    assert type(result) is dict
