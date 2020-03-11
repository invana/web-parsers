import locale
import re
import logging
import json
import ast

logger = logging.getLogger(__name__)


class FieldTransformerBase(object):
    """
    IntField(data="1").transform()

    """

    def get_method(self):
        """
        Should return the function that takes data as input. Ex: str, int, float,

        :return:
        """
        raise NotImplementedError("This method is not implemented")

    def __init__(self, data=None):
        self.data = data

    def try_or_none(self):
        transformation_method = self.get_method()
        if transformation_method:
            try:
                result_data = transformation_method(self.data)
            except Exception as e:
                logger.debug(e)
                result_data = self.data
            return result_data
        else:
            return self.data

    def transform(self):
        return self.try_or_none()


class StringField(FieldTransformerBase):

    def get_method(self):
        return str


class IntField(FieldTransformerBase):
    def get_method(self):
        def custom_int(data):
            if type(data) is str:
                data = locale.atoi(data)
            return int(data)
        return custom_int


class FloatField(FieldTransformerBase):
    def get_method(self):
        def custom_float(data):
            data = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", data)
            if len(data) > 0:
                return float(data[0])
            else:
                return float(0)

        return custom_float


class DictField(FieldTransformerBase):

    @staticmethod
    def dict_or_json_dump(d):
        if type(d) == dict:
            return d
        elif type(d) == str:
            return json.loads(d)
        return d

    def get_method(self):
        return  ast.literal_eval


class RawField(FieldTransformerBase):
    def get_method(self):
        return None
