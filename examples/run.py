from extraction_engine import ExtractionEngine
import yaml

from extraction_engine import ExtractionEngine
import yaml

html = open("page.html", "r").read()
# extraction_manifest = yaml.load(open("extract.yaml").read(),  yaml.Loader)
extraction_manifest_yaml = """
extractors:
- extractor_type: MetaTagExtractor
  extractor_id: meta_tags
- extractor_type: CustomContentExtractor
  extractor_id: content
  data_selectors:
  - selector_id: title
    selector: title
    selector_type: css
    selector_attribute: text
    data_type: RawField
"""
extraction_manifest = yaml.load(extraction_manifest_yaml, yaml.Loader)

engine = ExtractionEngine(html=html, extraction_manifest=extraction_manifest)
data = engine.extract_data()
print(data)
# {'meta_tags': {'meta__viewport': 'width=device-width, initial-scale=1', 'meta__google-site-verification': 'svzjE4Ll9L_SzXgYKt2YtOz6X6lYtCO0UrPDR0ZiRcM', 'title': 'Invana Knowledge Platform'}, 'content': {'title': 'Invana Knowledge Platform'}} {'meta_tags': {'meta__viewport': 'width=device-width, initial-scale=1', 'meta__google-site-verification': 'svzjE4Ll9L_SzXgYKt2YtOz6X6lYtCO0UrPDR0ZiRcM', 'title': 'Invana Knowledge Platform'}, 'content': {'title': 'Invana Knowledge Platform'}}
