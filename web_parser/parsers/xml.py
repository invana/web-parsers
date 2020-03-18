import xmltodict as xd
import json
from lxml import etree


class XMLParser:
    """




    """
    parsed_xml_data = None

    def __init__(self, xml_data, extractor_manifest=None):
        self.xml_data = xml_data
        self.extractor_manifest = extractor_manifest

    def to_dict(self):
        return json.loads(json.dumps(xd.parse(self.xml_data)))

    @staticmethod
    def parse_xml(xml_data):
        return etree.fromstring(xml_data)

    @staticmethod
    def get_nodes(xml_tree, xpath):
        return xml_tree.xpath(xpath)

    @staticmethod
    def extract_from_field(node, extractor_config, ):
        child_node = node.xpath(extractor_config.get("element_query", {}).get("value").lstrip("/"))[0]
        if extractor_config.get("data_attribute") == "text":
            return child_node.text or '' + ''.join(
                etree.tostring(e) for e in child_node)
        elif extractor_config.get("data_attribute") == "html":
            return etree.tostring(child_node, pretty_print=False)
        else:
            return child_node.attrib.get(
                extractor_config.get("data_attribute")
            )

    @staticmethod
    def get_nodes_from_data_type():
        pass

    def run_extractor(self, extractor):
        extractor_fields = extractor.get("extractor_fields", [])
        extracted_data = {}
        for extractor_field in extractor_fields:
            nodes = self.get_nodes(
                self.parsed_xml_data,
                extractor_field.get("element_query", {}).get("value")
            )
            child_selectors = extractor_field.get("child_selectors", [])

            if extractor_field.get("data_type").startswith("List"):
                extracted_items = []
                if extractor_field.get("data_attribute") == "element":
                    for node in nodes:
                        extracted_item = {}
                        for child_extractor in child_selectors:
                            extracted_item[child_extractor.get('field_id')] = self.extract_from_field(
                                node, child_extractor
                            )
                        extracted_items.append(extracted_item)
                    extracted_data[extractor_field.get('field_id')] = extracted_items
                else:
                    extracted_items = []
                    for node in nodes:
                        extracted_items.append(self.extract_from_field(
                            node, extractor_field
                        ))
                    extracted_data[extractor_field.get('field_id')] = extracted_items
            else:
                if extractor_field.get("data_attribute") == "element":
                    node = nodes[0]
                    extracted_item = {}
                    for child_extractor in child_selectors:
                        extracted_item[child_extractor.get('field_id')] = self.extract_from_field(
                            node, child_extractor
                        )
                    extracted_data[extractor_field.get('field_id')] = extracted_item
                else:
                    extracted_data[extractor_field.get('field_id')] = self.extract_from_field(
                        self.parsed_xml_data, extractor_field
                    )
        return extracted_data

    @staticmethod
    def flatten_extracted_data(all_extracted_data):
        all_extracted_data_new = {}
        for k, v in all_extracted_data.items():
            all_extracted_data_new.update(v)
        return all_extracted_data_new

    def run_extractors(self, flatten_extractors=False):
        self.parsed_xml_data = self.parse_xml(self.xml_data)

        all_extracted_data = {}
        for extractor in self.extractor_manifest:
            extracted_data = self.run_extractor(extractor)
            all_extracted_data[extractor.get("extractor_id")] = extracted_data

        if flatten_extractors is True:
            return self.flatten_extracted_data(all_extracted_data)
        return all_extracted_data
