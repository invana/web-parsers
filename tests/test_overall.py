from web_parser.parsers import HTMLParserEngine
from web_parser.utils import yaml_to_json
import os

path = os.getcwd()


def test_overall_web_parser_engine():
    html = open("{}/tests/page.html".format(path), "r").read()
    extraction_manifest = yaml_to_json(open("{}/tests/extract.yaml".format(path)).read())
    engine = HTMLParserEngine(html=html, url="http://localhost", extraction_manifest=extraction_manifest)
    result = engine.extract_data()
    assert result['meta_tags'] is not None
    assert result['content'] is not None
    assert type(result) is dict
    assert "content" in result
    assert "meta_tags" in result


def test_overall_web_parser_engine_failure_case():
    html = open("{}/tests/page.html".format(path), "r").read()
    extraction_manifest = yaml_to_json(open("{}/tests/extract-failcase.yaml".format(path)).read())
    engine = HTMLParserEngine(html=html, url="http://localhost", extraction_manifest=extraction_manifest)
    result = engine.extract_data()
    assert "meta_tags" not in result
    assert result['content'] is not None
    assert type(result) is dict


def test_overall_web_parser_engine_failure_invalid_extractor_type():
    html = open("{}/tests/page.html".format(path), "r").read()
    extraction_manifest = yaml_to_json(open("{}/tests/extract-failcase2.yaml".format(path)).read())
    engine = HTMLParserEngine(html=html, url="http://localhost", extraction_manifest=extraction_manifest)
    result = engine.extract_data()
    assert "meta_tag" in result
    assert result['meta_tag'] is None
    assert result['content'] is not None
    assert type(result) is dict
