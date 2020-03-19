from ..base import ContentExtractorBase
from web_parsers.utils.xml import extract_xml_field, get_nodes


class CustomDataExtractor(ContentExtractorBase):
    extracted_data = {}

    def add_to_field(self, field_data=None, extractor_field=None):
        if extractor_field.flatten_data:
            if field_data is not None:
                self.extracted_data.update(field_data)
        else:
            self.extracted_data[extractor_field.field_id] = field_data

    def run(self):
        extractor_fields = self.extractor.extractor_fields
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
                    self.add_to_field(field_data=extracted_items, extractor_field=extractor_field)
                else:
                    extracted_items = []
                    for node in nodes:
                        extracted_items.append(extract_xml_field(
                            node, extractor_field
                        ))
                    self.add_to_field(field_data=extracted_items, extractor_field=extractor_field)

            else:
                if extractor_field.data_attribute == "element":
                    node = nodes[0]
                    extracted_item = {}
                    for child_extractor in child_selectors:
                        extracted_item[child_extractor.field_id] = extract_xml_field(
                            node, child_extractor
                        )
                    self.add_to_field(field_data=extracted_item, extractor_field=extractor_field)

                else:
                    field_data = extract_xml_field(
                        self.html_selector, extractor_field
                    )
                    self.add_to_field(field_data=field_data, extractor_field=extractor_field)

        return {self.extractor_id: self.extracted_data}
