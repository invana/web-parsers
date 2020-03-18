# manifest.yml

Manifest is the configuration that contains both author information and the instructions to 
extract data from HTML/XML.


## Example

```python
from web_parser.manifest.v1 import HTMLExtractionManifest

manifest = HTMLExtractionManifest(
    title="invana.io blogs",
    domain="invana.io",
    version="beta",
    test_urls=["https://invana.io/blogs",],
    owner={
        "title": "Ravi Raja Merugu",
        "ownership_type": "Individual",
        "email": "rrmerugu@gmail.com",
        "website_url": "https://rrmerugu.github.io"
    },
    extractors=[] # <---- here comes the actual manifest 
)
```
## Types of Extractors

Web Parser provides three types of extractors for data extraction from HTML. 

1. Standard Extractors - extract data from standard html tags, like Paragraphs, Headings, Anchor tags, meta tags, 
JSON+LD, tables, ordered and unordered lists.
2. CustomData Extractor
3. Python Extractor

### Example Usage



This below extractor configuration will extract all `<meta>` tags data.
```yaml
- extractor_type: MetaTagExtractor
  extractor_id: meta_tags
```

```json
{
 "meta_tags": {
      "meta__description": "Connect to your databases, microservices  or data from internet and create Knowledge & Data APIs in near realtime",
      "meta__viewport": "width=device-width, initial-scale=1",
      "title": "Use Cases | Invana"
  }
}
```

```yaml
- extractor_type: ParagraphsExtractor
  extractor_id: paragraphs
```
```json
{
 "paragraphs": [
      "Connect to your databases, microservices  or data from internet and create Knowledge & Data APIs in near realtime",
  ]
}
```

## Standard Extractors

```python
from web_parser.extractors.html.content import DataExtractor, PageOverviewExtractor, \
    ParagraphsExtractor, HeadingsExtractor, TableContentExtractor, MetaTagExtractor, IconsExtractor, JSONLDExtractor, \
    FeedUrlExtractor, PlainHTMLContentExtractor, MainContentExtractor
```