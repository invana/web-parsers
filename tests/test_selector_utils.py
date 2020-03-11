from web_parser.utils.selectors import convert_html_to_selector, transform_data
import os
from parsel import Selector


def test_convert_html_to_selector():
    path = os.getcwd()
    html = open("{}/tests/page.html".format(path), "r").read()
    a = convert_html_to_selector(html)
    assert type(a) is Selector


def test_transform_data():
    a = transform_data(data="1", data_type="IntField")
    assert type(a) is int
    a = transform_data(data="1.1", data_type="FloatField")
    assert type(a) is float
