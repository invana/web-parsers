from web_parser.parsers.xml import XMLParser
import os


def test_xml_from_test():
    # use requests.get('https://invana.io/feed.xml').text with python-requests
    path = os.getcwd()
    xml_data = open("{}/tests/xml/feed.xml".format(path)).read()
    json_data = XMLParser(xml_data).run()
    assert type(json_data) is dict
    assert "rss" in json_data
