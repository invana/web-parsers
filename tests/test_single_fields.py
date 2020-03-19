from web_parsers.fields import FloatField, RawField, StringField, IntField, DictField


def test_string_field_transformer():
    a = StringField(data=1).transform()
    assert a == "1"


def test_int_field_transformer():
    a = IntField(data="123").transform()
    assert a == 123


def test_float_field_transformer():
    a = FloatField(data="1.2").transform()
    assert a == 1.2
    b = FloatField(data="1").transform()
    assert b == 1


def test_dict_field_transformer():
    a = DictField(data="{'hello':'world'}").transform()
    assert type(a) is dict
    assert a['hello'] == "world"

    a = DictField(data={'hello': 'world'}).transform()
    assert type(a) is dict
    assert a['hello'] == "world"

    a = DictField(data={"hello": "world"}).transform()
    assert type(a) is dict
    assert a['hello'] == "world"


def test_raw_field_transformer():
    a = RawField(data="{'hello':'world'}").transform()
    assert type(a) is str
    a = RawField(data="hello").transform()
    assert type(a) is str
    assert a == "hello"
    a = RawField(data=1).transform()
    assert type(a) is int
    assert a == 1
    a = RawField(data=1.1).transform()
    assert type(a) is float
    assert a == 1.1
