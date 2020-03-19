# HTML Extractor 



## Regular data extractor
```python
from web_parser import HTMLParser
from web_parser.manifest import WebParserManifest
import urllib.request
import yaml

html_string = urllib.request.urlopen("https://invana.io").read().decode("utf-8")
extraction_manifest_yaml = """
- extractor_type: CustomDataExtractor
  extractor_id: content
  extractor_fields:
  - field_id: title
    element_query: 
      type: css
      value: title
    data_attribute: text
    data_type: StringField
"""
extraction_manifest = yaml.load(extraction_manifest_yaml, yaml.Loader)

manifest = WebParserManifest(
    title="invana.io blogs",
    domain="invana.io",
    version="beta",
    test_urls="https://invana.io/blogs",
    owner={
        "title": "Ravi Raja Merugu",
        "ownership_type": "Individual",
        "email": "rrmerugu@gmail.com",
        "website_url": "https://rrmerugu.github.io"
    },
    extractors=extraction_manifest
)

engine = HTMLParser(html_string=html_string, url="http://dummy-url.com", extraction_manifest=manifest)
data = engine.run(flatten_extractors=False)
print(data)
{'content': {'title': 'Enrich your data with information available on the Internet | Invana'}}

data = engine.run(flatten_extractors=True) # this will remove the `content` which is the extractor id,
{'title': 'Enrich your data with information available on the Internet | Invana'}
```



## With child selectors
```python

from web_parser import HTMLParser
from web_parser.manifest import WebParserManifest
import urllib.request
import yaml

html_string = urllib.request.urlopen("https://invana.io/use-cases.html").read().decode("utf-8")
extraction_manifest_yaml = """
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
"""
extraction_manifest = yaml.load(extraction_manifest_yaml, yaml.Loader)

manifest = WebParserManifest(
    title="invana.io blogs",
    domain="invana.io",
    version="beta",
    test_urls="https://invana.io/blogs",
    owner={
        "title": "Ravi Raja Merugu",
        "ownership_type": "Individual",
        "email": "rrmerugu@gmail.com",
        "website_url": "https://rrmerugu.github.io"
    },
    extractors=extraction_manifest
)

engine = HTMLParser(html_string=html_string, url="http://dummy-url.com", extraction_manifest=manifest)
data = engine.run(flatten_extractors=False) 
print(data)
{'content': {'use_cases': [{'body': 'Automate anything on the web with '
                                    'browsers. Post data or crawl and fetch '
                                    'structured information from any a single '
                                    'webpage or from a pool of websites.',
                            'heading': 'Web Automation'},
                           {'body': "Invana GraphQL API's gives you instant "
                                    'APIs without coding, giving you  power to '
                                    'rapidly experiment with your data schemas '
                                    'that work for you.',
                            'heading': 'Rapid Prototyping'},
                           {'body': 'Invana gives you easy and potential to \n'
                                    '                        run microservices '
                                    'that range from simple text or image '
                                    'processing functions to Machine Learning '
                                    'models',
                            'heading': 'Run Microservices on stream'},
                           {'body': "Invana let's you analyse, compute and do "
                                    'operatoins on your stream data to produce '
                                    'knowledge and facts needed for your '
                                    'Machine Learning Projects.',
                            'heading': 'Build Knowledge Graphs'},
                           {'body': "Invana let's you crawl through data "
                                    'available on the internet or from your '
                                    'data buckets or databases and gives a '
                                    'scalable search API.',
                            'heading': 'Instantly Build Search APIs'}]}}

data = engine.run(flatten_extractors=True)
print(data)
{'use_cases': [{'body': 'Automate anything on the web with browsers. Post data '
                        'or crawl and fetch structured information from any a '
                        'single webpage or from a pool of websites.',
                'heading': 'Web Automation'},
               {'body': "Invana GraphQL API's gives you instant APIs without "
                        'coding, giving you  power to rapidly experiment with '
                        'your data schemas that work for you.',
                'heading': 'Rapid Prototyping'},
               {'body': 'Invana gives you easy and potential to \n'
                        '                        run microservices that range '
                        'from simple text or image processing functions to '
                        'Machine Learning models',
                'heading': 'Run Microservices on stream'},
               {'body': "Invana let's you analyse, compute and do operatoins "
                        'on your stream data to produce knowledge and facts '
                        'needed for your Machine Learning Projects.',
                'heading': 'Build Knowledge Graphs'},
               {'body': "Invana let's you crawl through data available on the "
                        'internet or from your data buckets or databases and '
                        'gives a scalable search API.',
                'heading': 'Instantly Build Search APIs'}]}

```


## Flatten Extracted data

```python
# look at the above example for a practical example with code.
engine = HTMLParser(html_string=html_string, url="http://dummy-url.com", extraction_manifest=manifest)
data = engine.run(flatten_extractors=True)
```