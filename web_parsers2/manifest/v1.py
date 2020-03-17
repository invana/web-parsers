from importlib import import_module

extractor_classes = import_module(f'web_parsers2.extractors.html')


class ExtractorManifestByElement:

    def __init__(self, field_name=None, data_type=None, selector_query=None, attributes=None):
        self.field_name = field_name
        self.data_type = data_type
        self.selector_query = selector_query
        self.attributes = attributes

    def __repr__(self):
        return "<ExtractorManifestByElement data_type='{data_type}' " \
               "selector_query='{selector_query}' " \
               "attributes_keys='{attributes_keys}' " \
               ">".format(data_type=self.data_type, selector_query=self.selector_query,
                          attributes_keys=self.attributes.keys())


class ExtractorManifestByField:

    def __init__(self, field_name=None, data_type=None, selector_query=None, data_attribute=None):
        self.field_name = field_name
        self.data_type = data_type
        self.selector_query = selector_query
        self.data_attribute = data_attribute

    def __repr__(self):
        return "<ExtractorManifestByField data_type='{data_type}' " \
               "selector_query='{selector_query}' " \
               "data_attribute='{data_attribute}' " \
               ">".format(data_type=self.data_type, selector_query=self.selector_query,
                          data_attribute=self.data_attribute)


class SingleExtractor:

    def __init__(self, extractor_type=None, extractor_id=None, extractor_items=None):
        self.extractor_type = extractor_type
        extractor_cls = getattr(extractor_classes, extractor_type)
        manifest = extractor_cls.manifest

        if manifest is not None:
            extractor_cls.manifest = ExtractorManifestByField(**manifest)
        self.extractor_cls = extractor_cls
        self.extractor_id = extractor_id
        self.extractor_items = extractor_items

    def to_dict(self):
        return {
            "extractor_type": self.extractor_type,
            "extractor_id": self.extractor_id,
            "extractor_items": self.extractor_items,

        }


    def __repr__(self):
        return "<SingleExtractor extractor_id=\"{extractor_id}\" " \
               "extractor_items=\"{extractor_items}\" >".format(extractor_id=self.extractor_id,
                                                                extractor_items=self.extractor_items)


class ExtractorManifest:

    def __init__(self,
                 title=None,
                 version=None,
                 author=None,
                 extract_by=None,
                 test_urls=None,
                 domain=None,
                 extractors=None
                 ):
        extractor_manifest_cls = None
        if extract_by not in ['element', 'field']:
            raise Exception("extract by can be only element or field")
        else:
            if extract_by == "element":
                extractor_manifest_cls = ExtractorManifestByElement
            elif extract_by == "field":
                extractor_manifest_cls = ExtractorManifestByField

        if version not in ['v1', ]:
            raise Exception("version  can be only v1")

        self.title = title
        self.test_urls = test_urls
        self.version = version
        self.domain = domain
        self.author = author
        self.extract_by = extract_by
        self.extractors = []

        for extractor in extractors:
            extractor_items = {}
            if extractor.get("extractor_items"):
                for field_name, manifest in extractor.get("extractor_items", {}).items():
                    extractor_items[field_name] = extractor_manifest_cls(field_name=field_name, **manifest)
                extractor['extractor_items'] = extractor_items
            else:
                extractor['extractor_items'] = None
            self.extractors.append(SingleExtractor(**extractor))
