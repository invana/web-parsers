from web_parser.utils.other import yaml_to_json
from web_parsers2.manifest.v1 import ExtractorManifest
from web_parsers2.managers.html import HTMLExtractionManager
import pprint

elements_extraction_manifest_example = """
extractor_type: CustomDataExtractor
extractor_id: heading_paragraph
extractor_items:
  headings:
    data_type: ListDictField
    selector_query:
      type: css
      value: h1
    attributes:
    - attribute: text
      field_name: text
      data_type: StringField
    - attribute: class
      field_name: class
      data_type: StringField    
    - attribute: element-id
      field_name: data_id
      data_type: IntField
  paragraphs:
    data_type: ListDictField
    selector_query:
      type: css
      value: p
    attributes:
    - attribute: text
      field_name: text
      data_type: StringField
    - attribute: html
      field_name: html
      data_type: StringField
    - attribute: class
      field_name: class
      data_type: StringField
    - attribute: element-id
      field_name: data_id
      data_type: IntField
"""

custom_extractor_example = """
extractor_type: CustomDataExtractor
extractor_id: heading_paragraph
extractor_items:
  headings:
    data_type: StringField
    selector_query:
      type: css
      value: h1
    data_attribute: text
  paragraphs:
    data_type: StringField
    selector_query:
      type: css
      value: p
    data_attribute: text
"""

html_string = """
<html>
<body>
<h1 class="title" element-id="1">Hello World h1</h1>
<h2 class="title" element-id="1">Hello World h2</h2>

<p element-id="2">This is the first paragraph</p>
<p element-id="3">This is the first three</p>
<p element-id="4">This is the first four</p>
<p element-id="5">This is the first five</p>
<p element-id="6">This is the first six</p>
<a href="/some-url">Somethings new</a>
<img src="image.jpeg" />

<table class="table">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">First</th>
      <th scope="col">Last</th>
      <th scope="col">Handle</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>Mark</td>
      <td>Otto</td>
      <td>@mdo</td>
    </tr>
    <tr>
      <th scope="row">2</th>
      <td>Jacob</td>
      <td>Thornton</td>
      <td>@fat</td>
    </tr>
    <tr>
      <th scope="row">3</th>
      <td>Larry</td>
      <td>the Bird</td>
      <td>@twitter</td>
    </tr>
  </tbody>
</table>
</body>
</html>
"""
elements_extraction_manifest_json = yaml_to_json(custom_extractor_example)
# elements_extraction_manifest_json = yaml_to_json(elements_extraction_manifest_example)
extractor_manifest_by_fields = ExtractorManifest(
    title="example_manifest",
    version="v1",
    test_urls=[""],
    domain="www.example.com",
    author={
        "name": "Ravi Raja Merugu",
        "email": "rrmerugu@gmail.com",
        "type": "Individual"
    }, extract_by="field",
    extractors=[
        elements_extraction_manifest_json,
        {
            "extractor_id": "paragraphs_list",
            "extractor_type": "ParagraphExtractor",
        },
        {
            "extractor_id": "headings",
            "extractor_type": "HeadingsExtractor",
        },
        {
            "extractor_id": "images",
            "extractor_type": "ImagesExtractor",
        },
        {
            "extractor_id": "links",
            "extractor_type": "LinksExtractor",
        },
        {
            "extractor_id": "tables",
            "extractor_type": "TableExtractor",
        }
    ]
)

manager = HTMLExtractionManager(
    html_string=html_string,
    url="http://example.com",
    generate_absolute_urls=True,
    extraction_manifest=extractor_manifest_by_fields
)
result = manager.run_extractors()
pprint.pprint(result, indent=4)
