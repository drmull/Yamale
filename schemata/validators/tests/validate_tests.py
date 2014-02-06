from ... import validators as val


def test_equality():
    assert val.String() == val.String()
    assert val.String(hello='wat') == val.String(hello='wat')
    assert val.String(hello='wat') != val.String(hello='nope')
    assert val.Boolean('yep') != val.Boolean('nope')


def test_integer():
    v = val.Integer()
    assert v.is_valid(1)
    assert not v.is_valid('1')
    assert not v.is_valid(1.34)


def test_string():
    v = val.String()
    assert v.is_valid('1')
    assert not v.is_valid(1)


def test_number():
    v = val.Number()
    assert v.is_valid(1)
    assert v.is_valid(1.3425235)
    assert not v.is_valid('str')


def test_boolean():
    v = val.Boolean()
    assert v.is_valid(True)
    assert v.is_valid(False)
    assert not v.is_valid('')
    assert not v.is_valid(0)


def test_list():
    v = val.List()
    assert v.is_valid([])
    assert v.is_valid(())
    assert not v.is_valid('')
    assert not v.is_valid(0)


def test_keywords():
    v = val.String(min=2)
    assert v.is_valid('abcd')
    assert v.is_valid('ab')
    assert not v.is_valid('a')

    v = val.Integer(max=10)
    assert v.is_valid(4)
    assert v.is_valid(10)
    assert not v.is_valid(11)

    v = val.Number(min=.5)
    assert v.is_valid(4)
    assert v.is_valid(.5)
    assert not v.is_valid(.1)
