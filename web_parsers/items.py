class ExtractedItem:

    def __init__(self, _id=None, field_name=None, data=None):
        self.data = data if data else None
        self._id = _id
        self.field_name = field_name

    def get_dict(self):
        """
        returns the data in json format
        :return:
        """
        if self.field_name:
            return {
                self.field_name: self.data
            }
        else:
            return self.data

    def __repr__(self):
        return "<ExtractedItem field_name=\"{field_name}\" data=\"{data}\" >".format(
            field_name=self.field_name,
            data=self.data
        )
