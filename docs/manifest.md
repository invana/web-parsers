# manifest.yml

Manifest is the configuration that contains both author information and the instructions to 
extract data from HTML/XML.


## Example Usage

```python
from web_parsers.manifest import WebParserManifest

manifest = WebParserManifest(
    title="invana.io blogs",
    domain="invana.io",
    version="alpha",
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
## 1. Types of Extractors

Web Parsers provides three types of extractors for data extraction from HTML. 

1. Standard Extractors - extract data from standard html tags
2. Custom Data Extractor -  extract data using your own elements and data attribute extraction
3. Python Extractor


### 1. Standard Extractors

To cover the most standard needs of data extraction, we have built standard extractors, which
extract from standard html tags like Paragraphs, Headings, Anchor tags, meta tags, 
JSON+LD, tables, ordered and unordered lists.


 
```python
from web_parsers.extractors.html.content import  PageOverviewExtractor, \
    ParagraphsExtractor, HeadingsExtractor, TableContentExtractor, MetaTagExtractor, IconsExtractor, JSONLDExtractor, \
    FeedUrlExtractor, PlainHTMLContentExtractor, MainContentExtractor
```


#### 1.1 MetaTagExtractor Example
This below extractor configuration will extract all `<meta>` tags data.
```yaml
- extractor_type: MetaTagExtractor
  extractor_id: meta_tags
 
# result  
{
 "meta_tags": {
      "meta__description": "Connect to your databases, microservices  or data from internet and create Knowledge & Data APIs in near realtime",
      "meta__viewport": "width=device-width, initial-scale=1",
      "title": "Use Cases | Invana"
  }
}
```

#### 1.2 ParagraphsExtractor Example
```yaml
- extractor_type: ParagraphsExtractor
  extractor_id: paragraphs
 
# result   
{
 "paragraphs": [
      "Connect to your databases, microservices  or data from internet and create Knowledge & Data APIs in near realtime",
  ]
}
```

#### 1.3 PageOverviewExtractor Example
```yaml
- extractor_type: PageOverviewExtractor
  extractor_id: overview
 
# result   
{'overview': {
    'canonical_url': None,
    'description': 'Connect to your databases, microservices or data  from internet and create Knowledge & Data APIs '
                 'in near realtime',
    'domain': 'invana.io',
    'first_paragraph': 'Invana is an open source distributed processing engine aiming to allow you run '
                     'microservices on top of your data(static or streams), giving you a',
    'image': None,
    'keywords': None,
    'page_type': None,
    'shortlink_url': None,
    'title': 'Enrich your data with information available on the Internet | Invana',
    'url': None
  }
}
```


### 2. Custom Data Extractor

We need to define data extractor configuration in yaml format, with each field_id to extract in 
the format field.

All the custom data extractor should have `extractor_fields` defined along with `extractor_id` and `extractor_type`. 
Each data field should be defined as:

```yaml
  - field_id: title
    element_query:
      type: css
      value: title
    data_attribute: text
    data_type: StringField
```  


### 2.1 Extracting flat data.

```yaml
- extractor_type: CustomDataExtractor
  extractor_id: content
  extractor_fields:
  - field_id: title
    element_query:
      type: css
      value: title
    data_attribute: text
    data_type: StringField
  - field_id: first_paragraph
    element_query:
      type: css
      value: p
    data_attribute: text
    data_type: StringField
  - field_id: image
    element_query:
      type: css
      value: .hero-image
    data_attribute: src
    data_type: StringField

#result 
{
  "title": "Invana",
  "first_paragraph": "Invana is an open source distributed processing engine aiming to allow you run 
microservices on top of your data(static or streams), giving you a production-ready Knowledge and 
Data APIs in near realtime."
  "image": "https://invana.io/image/hero-image.png"

}
```
### 2.2 Extracting items with sub data. 

To extract data like product items from e-commerce sites like amazon or blogs 
from any sites, we need to extract list of blogs data including the fields like
 title, price, image, description etc.
 
That is when we should use something like below, which lets us extract html elements with 
`selector_query` and assign `ListDictField` as we are going to extract list of dictionary elements. 
```yaml
data_attribute: element
data_type: ListDictField
```

The full configuration would look like this, 

```yaml
- extractor_type: CustomDataExtractor
  extractor_id: content
  extractor_fields:
  - field_id: use_cases
    element_query:
      type: css
      value: .card-body
    data_attribute: element
    data_type: ListDictField
    child_selectors:
      - field_id: heading
        element_query:
          type: css
          value: h3
        data_attribute: text
        data_type: StringField
      - field_id: body
        element_query:
          type: css
          value: p
        data_attribute: text
        data_type: StringField

#result 

{'use_cases': [
    {
      'body': 'Automate anything on the web ...'
      'heading': 'Web Automation ...'
    },...
  ]
}
```


## 2. Types of Data types

Each `field_id`, should be assigned a data type, so that the data will be saved in the format, that can 
be used for indexing the data. Valid data types are :

1. RawField
2. ListRawField
3. StringField
4. ListStringField
5. IntField
6. ListIntField
7. FloatField
8. ListFloatField
9. DictField
10. ListDictField



