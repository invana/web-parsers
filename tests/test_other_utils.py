from web_parser.utils.other import yaml_to_json, generate_random_id
import os


def test_generate_random_id():
    a = generate_random_id()
    assert type(a) is str


def test_yaml_to_json():
    path = os.getcwd()
    a = yaml_to_json(open("{}/tests/configs/extract-python.yaml".format(path)).read())
    assert type(a) is dict
    assert a['extractor_type'] == "PythonExtractorManifest"
