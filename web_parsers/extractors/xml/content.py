from ..base import ContentExtractorBase
from web_parsers.utils.xml import extract_xml_field, get_nodes


class CustomDataExtractor(ContentExtractorBase):

    @staticmethod
    def flatten_data(data=None):
        if data is None:
            return data
        return data.values[0]

    def run(self):
        extractor_fields = self.extractor.extractor_fields
        extracted_data = {}
        for extractor_field in extractor_fields:
            nodes = get_nodes(
                self.html_selector,
                extractor_field.element_query.get("value")
            )
            child_selectors = extractor_field.child_selectors
            if extractor_field.data_type.startswith("List"):
                extracted_items = []
                if extractor_field.data_attribute == "element":
                    for node in nodes:
                        extracted_item = {}
                        for child_extractor in child_selectors:
                            extracted_item[child_extractor.field_id] = extract_xml_field(
                                node, child_extractor
                            )
                        extracted_items.append(extracted_item)
                    extracted_data[extractor_field.field_id] = extracted_items
                else:
                    extracted_items = []
                    for node in nodes:
                        extracted_items.append(extract_xml_field(
                            node, extractor_field
                        ))
                    extracted_data[extractor_field.field_id] = extracted_items
            else:
                if extractor_field.data_attribute == "element":
                    node = nodes[0]
                    extracted_item = {}
                    for child_extractor in child_selectors:
                        extracted_item[child_extractor.field_id] = extract_xml_field(
                            node, child_extractor
                        )
                    extracted_data[extractor_field.field_id] = extracted_item
                else:
                    extracted_data[extractor_field.field_id] = extract_xml_field(
                        self.html_selector, extractor_field
                    )
        return extracted_data
