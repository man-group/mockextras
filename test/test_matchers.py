from mockextras import Any, Contains, AnyOf


def test_any_equality():
    assert Any() == "hello"
    assert "hello" == Any()

    assert Any() == []
    assert [] == Any()

    assert Any() == 100
    assert 100 == Any()

    assert Any() == []
    assert [] == Any()

    assert Any() == 100
    assert 100 == Any()

    assert Any(str) == "hello"
    assert "hello" == Any(str)

    assert Any(list) != "hello"
    assert "hello" != Any(list)

    assert Any(list) == []
    assert [] == Any(list)


def test_pretty_print_any():
    a = Any()
    assert repr(a) == "Any()"
    assert str(a) == "Any()"
    b = Any(str)
    assert repr(b) == "Any(<type 'str'>)" or repr(b) == "Any(<class 'str'>)"
    assert str(b) == "Any(<type 'str'>)" or str(b) == "Any(<class 'str'>)"


def test_contains_equality():
    assert Contains('h') == "hello"
    assert Contains('hell') == "hello"
    assert Contains('hello world') != "hello"
    assert Contains('fish') != "hello"

    assert "hello" == Contains('h')
    assert "hello" == Contains('hell')
    assert "hello" != Contains('hello world')
    assert "hello" != Contains('fish')

    assert range(100) == Contains(25)
    assert range(100) != Contains(125)

    assert dict(a=1, b=2, c=3) == Contains('a')
    assert dict(a=1, b=2, c=3) != Contains('d')
    assert Contains('a') == dict(a=1, b=2, c=3)
    assert Contains('d') != dict(a=1, b=2, c=3)


def test_pretty_print_contains():
    a = Contains(10)
    assert repr(a) == "Contains(10)"
    assert str(a) == "Contains(10)"

    b = Contains('hello')
    assert repr(b) == "Contains('hello')"
    assert str(b) == "Contains('hello')"


def test_any_of_equality():
    assert AnyOf() != "hello"
    assert AnyOf("fox") != "hello"
    assert AnyOf("fox", "badger", "monkey") != "hello"
    assert AnyOf('hello') == "hello"
    assert AnyOf('hello', 'world', 'hoorah') == "hello"

    assert "hello" != AnyOf()
    assert "hello" != AnyOf("fox")
    assert "hello" != AnyOf("fox", "badger", "monkey")
    assert "hello" == AnyOf('hello')
    assert "hello" == AnyOf('hello', 'world', 'hoorah')


def test_pretty_print_any_of():
    a = AnyOf()
    assert repr(a) == "AnyOf()"
    assert str(a) == "AnyOf()"

    a = AnyOf(10)
    assert repr(a) == "AnyOf(10)"
    assert str(a) == "AnyOf(10)"

    b = AnyOf(10, 20, 30)
    assert repr(b) == "AnyOf(10, 20, 30)"
    assert str(b) == "AnyOf(10, 20, 30)"
