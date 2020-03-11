from web_parser.fields import ListFloatField, ListIntField, ListDictField, ListRawField, ListStringField


def test_string_list_field_transformer():
    a = ListStringField(data=["1", 2, "4", 5.5]).transform()
    assert type(a) is list
    assert a == ["1", "2", "4", "5.5"]


def test_int_list_field_transformer():
    a = ListIntField(data=["1", "2", 3, 4.1]).transform()
    assert type(a) is list
    assert a == [1, 2, 3, 4]


def test_float_list_field_transformer():
    a = ListFloatField(data=["1.2", 1, 3.3]).transform()
    assert type(a) is list
    assert a == [1.2, 1, 3.3]


def test_dict_field_transformer():
    a = ListDictField(data=["{'hello':'world'}", {"hello": "world2"}]).transform()
    assert type(a) is list
    assert a[0] == {"hello": "world"}
    assert a[1] == {"hello": "world2"}


def test_raw_field_transformer():
    a = ListRawField(data=["{'hello':'world'}", {"hello": "world2"}, 1, 2.3, "hello"]).transform()
    assert type(a) is list
    assert type(a[0]) is str
    assert type(a[1]) is dict
    assert type(a[2]) is int
    assert type(a[3]) is float
    assert type(a[4]) is str
