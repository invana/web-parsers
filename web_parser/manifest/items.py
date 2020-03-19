class ItemManifest:

    def __init__(self,
                 field_id=None,
                 data_type="RawField",
                 element_query=None,
                 data_attribute=None,
                 child_selectors=None
                 ):
        self.field_id = field_id
        self.data_type = data_type
        self.element_query = element_query
        self.data_attribute = data_attribute
        if child_selectors:
            self.child_selectors = [ItemManifest(**child_selector) for child_selector in
                                    child_selectors]
        else:
            self.child_selectors = []

    def __repr__(self):
        return "<ItemManifest data_type='{data_type}' " \
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
