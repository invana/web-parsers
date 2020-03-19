from lxml import etree


def parse_xml(string_data):
    return etree.fromstring(string_data)


def get_nodes(xml_tree, xpath):
    return xml_tree.xpath(xpath)


def get_node_text(node):
    return node.text or '' + ''.join(
        etree.tostring(e) for e in node)


def get_node_html(node):
    return etree.tostring(node, pretty_print=False)


def extract_xml_field(node, extractor_config):
    child_node = node.xpath(extractor_config.element_query.get("value").lstrip("/"))[0]
    if extractor_config.data_attribute == "text":
        return get_node_text(child_node)
    elif extractor_config.data_attribute == "html":
        return get_node_html(child_node)
    else:
        return child_node.attrib.get(
            extractor_config.data_attribute
        )
