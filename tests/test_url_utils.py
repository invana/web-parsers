from web_parser.utils.url import get_absolute_url, get_domain, get_urn


def test_get_urn():
    a = get_urn(" https://blog.scrapinghub.com/page/6/")
    assert a == "blog.scrapinghub.com/page/6/"


def test_get_domain():
    a = get_domain("https://blog.scrapinghub.com/page/6/")
    assert a == "blog.scrapinghub.com"


def test_get_absolute_url():
    a = get_absolute_url(url="/feed.xml", origin_url="https://blog.scrapinghub.com/page/6/")
    assert a == "https://blog.scrapinghub.com/feed.xml"

    a = get_absolute_url(url="feed.xml", origin_url="https://blog.scrapinghub.com/page/6/")
    assert a == "https://blog.scrapinghub.com/feed.xml"

    a = get_absolute_url(url="./feed.xml", origin_url="https://blog.scrapinghub.com/page/6/")
    assert a == "https://blog.scrapinghub.com/feed.xml"

    a = get_absolute_url(url="https://blog.scrapinghub.com/feed.xml", origin_url="https://blog.scrapinghub.com/page/6/")
    assert a == "https://blog.scrapinghub.com/feed.xml"
