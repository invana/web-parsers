from web_parser.utils.other import yaml_to_json
from web_parsers2.manifest.v1 import ExtractorManifest
from web_parsers2.managers.html import HTMLExtractionManager

elements_extraction_manifest_example = """
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
<h1 class="title" element-id="1">Hello World</h1>
<p element-id="2">This is the first paragraph</p>

</body>
</html>
"""
custom_extractor_example = yaml_to_json(custom_extractor_example)
# print("custom_extractor_example", custom_extractor_example)
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
        custom_extractor_example,
        {
            "extractor_id": "paragraphs_list",
            "extractor_type": "ParagraphExtractor",

        }]
)

manager = HTMLExtractionManager(
    html_string=html_string,
    url="http://example.com",
    extraction_manifest=extractor_manifest_by_fields
)

aa = manager.run_extractors()

print(aa.keys())
print(aa)
