from mockextras import Any, Contains, AnyOf
import pytest


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


def is_positive(number):
    return number >= 0


@pytest.mark.parametrize(
    "predicates,matches,not_matches",
    (
        ([lambda x: x == "hello"], ["hello"], ["world"]),
        ([bool], [[1], 1, True], [[], 0, False, None]),
        ([lambda x: x > 75], [100], [50]),
        ([lambda x: len(x) > 3, lambda x: x[0] == "h"], ["hello"], ["hi", "greetings", ""]),
        ([is_positive], [2], [-2]),
    )
)
def test_any_such_that_equality(predicates, matches, not_matches):
    matcher = reduce(lambda m, p: m.such_that(p), predicates, Any())

    for match in matches:
        assert matcher == match
        assert match == matcher

    for not_match in not_matches:
        assert matcher != not_match
        assert not_match != matcher


def test_any_such_that_equality_typed():
    assert Any(str).such_that(lambda x: len(x) > 3) == "hello"
    assert "hello" == Any(str).such_that(lambda x: len(x) > 3)

    assert Any(str).such_that(lambda x: len(x) > 3) != ["h", "e", "l", "l", "o"]
    assert ["h", "e", "l", "l", "o"] != Any(str).such_that(lambda x: len(x) > 3)


def test_any_such_that_not_mutated():
    """Ensure that `such_that` operates on a new copy of the matcher instead
    of mutating the old one.
    """
    a = Any(str).such_that(lambda s: s[0] == "a")
    b = a.such_that(lambda s: s[1] == "b")
    c = a.such_that(lambda s: s[1] == "c")

    assert b == "able"
    assert "able" == b
    assert b is not a

    assert c == "act"
    assert "act" == c
    assert c is not a


def test_pretty_print_any_such_that():
    def my_predicate(x):
        return True

    a = Any()
    aa = a.such_that(my_predicate).such_that(lambda: True)
    assert repr(aa) == repr(a) + ".such_that(my_predicate).such_that(<lambda>)"
    assert str(aa) == str(a) + ".such_that(my_predicate).such_that(<lambda>)"

    class Predicate(object):
        @classmethod
        def __call__(cls, x):
            return True

    b = Any(str)
    bb = b.such_that(Predicate)
    assert repr(bb) == repr(b) + ".such_that(Predicate)"
    assert str(bb) == str(b) + ".such_that(Predicate)"


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
