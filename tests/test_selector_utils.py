from web_parser.utils.selectors import convert_html_to_selector
import os
from parsel import Selector


def test_convert_html_to_selector():
    path = os.getcwd()
    html = open("{}/tests/page.html".format(path), "r").read()
    a = convert_html_to_selector(html)
    assert type(a) is Selector
