class FieldManifest:

    def __init__(self,
                 field_id=None,
                 data_type="RawField",
                 element_query=None,
                 data_attribute=None,
                 child_selectors=None,
                 flatten_data=False
                 ):
        self.field_id = field_id
        self.data_type = data_type
        self.element_query = element_query
        self.data_attribute = data_attribute

        if (data_attribute != "element" and flatten_data is True) or (
                data_attribute == "element" and data_type != "DictField" and flatten_data is True):
            raise Exception(
                "error on `{field_id}` field manifest : flatten_data=True, can only be used with "
                "data_attribute=='element' and data_type=='DictField'".format(field_id=field_id)
            )

        self.flatten_data = flatten_data

        if child_selectors:
            self.child_selectors = [FieldManifest(**child_selector) for child_selector in
                                    child_selectors]
        else:
            self.child_selectors = []

    def __repr__(self):
        return "<FieldManifest data_type='{data_type}' " \
               "element_query='{element_query}' " \
               "data_attribute='{data_attribute}' " \
               ">".format(data_type=self.data_type, element_query=self.element_query,
                          data_attribute=self.data_attribute)

    def to_dict(self):
        return {
            "field_id": self.field_id,
            "element_query": self.element_query,
            "data_type": self.data_type,
            "data_attribute": self.data_attribute
        }
