from mockextras import when, Any
try:
    from unittest.mock import Mock, MagicMock, sentinel
except ImportError:
    from mock import Mock, MagicMock, sentinel
import pytest


def test_when_with_mock():
    mock_fn = Mock()
    when(mock_fn).called_with(sentinel.arg).then(sentinel.result)

    assert mock_fn(sentinel.arg) == sentinel.result


def test_when_with_magic_mock():
    mock_fn = MagicMock()
    when(mock_fn).called_with(sentinel.arg).then(sentinel.result)

    assert mock_fn(sentinel.arg) == sentinel.result


def test_can_not_use_when_with_non_mock():
    mock_fn = lambda _ : 10

    with pytest.raises(RuntimeError):
        when(mock_fn)


def test_can_not_use_when_with_mock_that_has_already_got_a_side_effect():
    with pytest.raises(RuntimeError):
        when(Mock(side_effect=lambda _ : 10))

    with pytest.raises(RuntimeError):
        when(Mock(side_effect=[1, 2, 3, 4]))


def test_when_with_any():
    mock_fn = Mock()
    when(mock_fn).called_with(Any()).then(sentinel.result1)
    when(mock_fn).called_with(sentinel.arg1, Any()).then(sentinel.result2)
    when(mock_fn).called_with(sentinel.arg2, Any(list)).then(sentinel.result3)
    when(mock_fn).called_with(sentinel.arg2, Any(str)).then(sentinel.result4)

    assert mock_fn(sentinel.arg1) == sentinel.result1
    assert mock_fn(sentinel.arg2) == sentinel.result1
    assert mock_fn("hello") == sentinel.result1
    assert mock_fn(100) == sentinel.result1
    assert mock_fn(sentinel.arg1, "hello") == sentinel.result2
    assert mock_fn(sentinel.arg1, "world") == sentinel.result2
    assert mock_fn(sentinel.arg2, []) == sentinel.result3
    assert mock_fn(sentinel.arg2, [1, 2, 3]) == sentinel.result3
    assert mock_fn(sentinel.arg2, ["hello", "world"]) == sentinel.result3
    assert mock_fn(sentinel.arg2, "world") == sentinel.result4


def test_when_call_then_return():
    mock_fn = Mock()
    when(mock_fn).called_with().then(sentinel.result0)
    when(mock_fn).called_with(sentinel.arg1).then(sentinel.result1)
    when(mock_fn).called_with(sentinel.arg2).then(sentinel.result2)
    when(mock_fn).called_with(sentinel.arg1, sentinel.arg2).then(sentinel.result3)
    when(mock_fn).called_with(sentinel.arg1, sentinel.arg1).then(sentinel.result4)
    when(mock_fn).called_with(sentinel.arg1, other=sentinel.other).then(sentinel.result5)
    when(mock_fn).called_with(x=sentinel.x, y=sentinel.y).then(sentinel.result6)

    assert mock_fn() == sentinel.result0
    assert mock_fn(sentinel.arg1) == sentinel.result1
    assert mock_fn(sentinel.arg2) == sentinel.result2
    assert mock_fn(sentinel.arg1, sentinel.arg2) == sentinel.result3
    assert mock_fn(sentinel.arg1, sentinel.arg1) == sentinel.result4
    assert mock_fn(sentinel.arg1, other=sentinel.other) == sentinel.result5
    assert mock_fn(x=sentinel.x, y=sentinel.y) == sentinel.result6


def test_when_call_then__return_single():
    mock_fn = Mock()
    when(mock_fn).called_with(sentinel.arg1).then(sentinel.result1)

    assert mock_fn(sentinel.arg1) == sentinel.result1
    assert mock_fn(sentinel.arg1) == sentinel.result1


def test_when_call_then_return_multiple():
    mock_fn = Mock()
    when(mock_fn).called_with(sentinel.arg1).then(sentinel.result1)\
                                            .then(sentinel.result2)\
                                            .then(sentinel.result3)

    assert mock_fn(sentinel.arg1) == sentinel.result1
    assert mock_fn(sentinel.arg1) == sentinel.result2
    assert mock_fn(sentinel.arg1) == sentinel.result3
    assert mock_fn(sentinel.arg1) == sentinel.result3


class TestException(Exception):
    pass


def test_when_call_then_raise():
    mock_fn = Mock()
    when(mock_fn).called_with().then(TestException(sentinel.exception0))
    when(mock_fn).called_with(sentinel.arg1).then(TestException(sentinel.exception1))
    when(mock_fn).called_with(sentinel.arg2).then(TestException(sentinel.exception2))
    when(mock_fn).called_with(sentinel.arg1, sentinel.arg2).then(TestException(sentinel.exception3))
    when(mock_fn).called_with(sentinel.arg1, sentinel.arg1).then(TestException(sentinel.exception4))
    when(mock_fn).called_with(sentinel.arg1, other=sentinel.other).then(TestException(sentinel.exception5))
    when(mock_fn).called_with(x=sentinel.x, y=sentinel.y).then(TestException(sentinel.exception6))

    with pytest.raises(TestException) as err:
        mock_fn()
    assert str(err.value) == str(sentinel.exception0)

    with pytest.raises(TestException) as err:
        mock_fn(sentinel.arg1)
    assert str(err.value) == str(sentinel.exception1)

    with pytest.raises(TestException) as err:
        mock_fn(sentinel.arg2)
    assert str(err.value) == str(sentinel.exception2)

    with pytest.raises(TestException) as err:
        mock_fn(sentinel.arg1, sentinel.arg2)
    assert str(err.value) == str(sentinel.exception3)

    with pytest.raises(TestException) as err:
        mock_fn(sentinel.arg1, sentinel.arg1)
    assert str(err.value) == str(sentinel.exception4)

    with pytest.raises(TestException) as err:
        mock_fn(sentinel.arg1, other=sentinel.other)
    assert str(err.value) == str(sentinel.exception5)

    with pytest.raises(TestException) as err:
        mock_fn(x=sentinel.x, y=sentinel.y)
    assert str(err.value) == str(sentinel.exception6)


def test_when_call_then_raise_single():
    mock_fn = Mock()
    when(mock_fn).called_with(sentinel.arg1).then(TestException(sentinel.exception1))

    with pytest.raises(TestException) as err:
        mock_fn(sentinel.arg1)
    assert str(err.value) == str(sentinel.exception1)

    with pytest.raises(TestException):
        mock_fn(sentinel.arg1)


def test_when_call_then_raise_multiple():
    mock_fn = Mock()
    when(mock_fn).called_with(sentinel.arg1).then(TestException(sentinel.exception1))\
                                            .then(TestException)\
                                            .then(TestException(sentinel.exception3))

    with pytest.raises(TestException) as err:
        mock_fn(sentinel.arg1)
    assert str(err.value) == str(sentinel.exception1)

    with pytest.raises(TestException) as err:
        mock_fn(sentinel.arg1)
    assert str(err.value) == ""

    with pytest.raises(TestException) as err:
        mock_fn(sentinel.arg1)
    assert str(err.value) == str(sentinel.exception3)

    with pytest.raises(TestException):
        mock_fn(sentinel.arg1)


def test_when_call_then_mixed():
    mock_fn = Mock()
    when(mock_fn).called_with(sentinel.arg1).then(sentinel.result1)\
                                            .then(TestException(sentinel.exception2))\
                                            .then(TestException)\
                                            .then(sentinel.result3)

    assert mock_fn(sentinel.arg1) == sentinel.result1

    with pytest.raises(TestException):
        mock_fn(sentinel.arg1)

    with pytest.raises(TestException):
        mock_fn(sentinel.arg1)

    assert mock_fn(sentinel.arg1) == sentinel.result3
    assert mock_fn(sentinel.arg1) == sentinel.result3


def test_when_missing_case():
    mock_fn = Mock()
    when(mock_fn).called_with(sentinel.arg1).then(sentinel.result1)

    with pytest.raises(KeyError):
        mock_fn(sentinel.arg2)


def test_duplicate_called_with_statements_second_ignored():
    mock = Mock()
    when(mock).called_with(100, 200).then("monkey")
    when(mock).called_with(100, 200).then("hello")

    assert 'monkey' == mock(100, 200)
    assert 'hello' != mock(100, 200)


def test_most_general_last():
    mock = Mock()
    when(mock).called_with(100, 200).then("monkey")
    when(mock).called_with(100, Any()).then("hello")

    assert 'monkey' == mock(100, 200)
    assert 'hello' == mock(100, 300)
    assert 'hello' == mock(100, "monkey")
    assert 'hello' == mock(100, { "key" : 1000 })


def test_called_with_object_has_empty_string_representation():
    mock_fn = MagicMock()
    assert repr(when(mock_fn).called_with(sentinel.arg)) == ""
