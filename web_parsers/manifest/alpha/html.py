from importlib import import_module
import logging
from ..items import FieldManifest

logger = logging.getLogger(__name__)
extractor_classes = import_module(f'web_parsers.extractors.html')


class HTMLExtractorManifest:

    def __init__(self, extractor_type=None, extractor_id=None, extractor_fields=None):
        self.extractor_type = extractor_type
        try:
            extractor_cls = getattr(extractor_classes, extractor_type)
        except AttributeError as e:
            logger.error("Failed to import the extractor_type:{extractor_type} with error {error}".format(
                extractor_type=extractor_type,
                error=e
            ))
            extractor_cls = None
        self.extractor_cls = extractor_cls
        self.extractor_id = extractor_id
        if extractor_fields:
            self.extractor_fields = [FieldManifest(**item_manifest) for item_manifest in
                                     extractor_fields]
        else:
            self.extractor_fields = None

    def to_dict(self):
        return {
            "extractor_type": self.extractor_type,
            "extractor_id": self.extractor_id,
            "extractor_fields": self.extractor_fields,
        }

    def __repr__(self):
        return "<HTMLExtractorManifest extractor_id=\"{extractor_id}\" " \
               "extractor_fields=\"{extractor_fields}\" >".format(extractor_id=self.extractor_id,
                                                                  extractor_fields=self.extractor_fields)
