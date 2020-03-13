import xmltodict as xd
import json


class XMLParser:

    def __init__(self, xml_data):
        self.xml_data = xml_data

    def run(self):
        return json.loads(json.dumps(xd.parse(self.xml_data)))
