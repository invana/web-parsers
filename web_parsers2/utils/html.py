
from lxml.etree import fromstring, Element


def convert_string_to_html_tree(html_string):
    return fromstring(html_string)