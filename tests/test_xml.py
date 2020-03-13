from web_parser.parsers.xml import XMLParser
import os
import urllib.request


def test_xml_from_test():
    # use requests.get('https://invana.io/feed.xml').text with python-requests
    path = os.getcwd()
    xml_data = open("{}/tests/xml/feed.xml".format(path)).read()
    json_data = XMLParser(xml_data).run()
    assert type(json_data) is dict
    assert "rss" in json_data


def test_xml_from_remote_url():
    xml_data = urllib.request.urlopen("https://invana.io/feed.xml").read()
    json_data = XMLParser(xml_data).run()
    assert type(json_data) is dict
    assert "rss" in json_data


def test_xml_from_test_from_string():
    # use requests.get('https://invana.io/feed.xml').text with python-requests
    xml_data = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>Enrich your data with information available on the Internet | Invana</title>
        <description>Connect to your databases, microservices or data from internet and create Knowledge &amp; Data APIs
            in near realtime
        </description>
        <link>https://invana.io</link>
        <atom:link href="https://invana.io/feed.xml" rel="self" type="application/rss+xml"/>

        <item>
            <title>Enrich your data with information available on the Internet | Invana</title>
            <description>Connect to your databases, microservices or data from internet and create Knowledge &amp; Data
                APIs in near realtime
            </description>
            <link>/</link>
            <guid isPermaLink="true">https://invana.io/</guid>
        </item>

        <item>
            <title>Blog - Updates and stories | Invana</title>
            <description>Official blog of Invana</description>
            <link>/blog</link>
            <guid isPermaLink="true">https://invana.io/blog</guid>
        </item>

        <item>
            <title>Hello World!</title>
            <description>
            </description>
            <pubDate>2020-01-22T09:25:20+0000</pubDate>
            <link>https://invana.io/blog/hello-world.html</link>
            <guid isPermaLink="true">https://invana.io/blog/hello-world.html</guid>
        </item>

    </channel>
</rss>"""
    json_data = XMLParser(xml_data).run()
    assert type(json_data) is dict
    assert "rss" in json_data
