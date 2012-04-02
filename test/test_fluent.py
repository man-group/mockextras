from fluent import when
from matchers import Any
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
    mock_fn = lambda x : 10
    
    with pytest.raises(RuntimeError):
        when(mock_fn)
    
    
def test_can_not_use_when_with_mock_that_has_already_got_a_side_effect():
    with pytest.raises(RuntimeError):
        when(Mock(side_effect=lambda x : 10))

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
    
    try:
        mock_fn()
    except TestException as e:
        assert e.message == sentinel.exception0
    else:
        assert False
        
    try:
        mock_fn(sentinel.arg1)
    except TestException as e:
        assert e.message == sentinel.exception1
    else:
        assert False
        
    try:
        mock_fn(sentinel.arg2)
    except TestException as e:
        assert e.message == sentinel.exception2
    else:
        assert False
        
    try:
        mock_fn(sentinel.arg1, sentinel.arg2)
    except TestException as e:
        assert e.message == sentinel.exception3
    else:
        assert False
        
    try:
        mock_fn(sentinel.arg1, sentinel.arg1)
    except TestException as e:
        assert e.message == sentinel.exception4
    else:
        assert False
        
    try:
        mock_fn(sentinel.arg1, other=sentinel.other)
    except TestException as e:
        assert e.message == sentinel.exception5
    else:
        assert False
        
    try:
        mock_fn(x=sentinel.x, y=sentinel.y)
    except TestException as e:
        assert e.message == sentinel.exception6
    else:
        assert False


def test_when_call_then_raise_single():
    mock_fn = Mock()
    when(mock_fn).called_with(sentinel.arg1).then(TestException(sentinel.exception1))
    
    try:
        mock_fn(sentinel.arg1)
    except TestException as e:
        assert e.message == sentinel.exception1
    else:
        assert False
    
    with pytest.raises(TestException):
        mock_fn(sentinel.arg1)


def test_when_call_then_raise_multiple():
    mock_fn = Mock()
    when(mock_fn).called_with(sentinel.arg1).then(TestException(sentinel.exception1))\
                                            .then(TestException)\
                                            .then(TestException(sentinel.exception3))

    try:
        mock_fn(sentinel.arg1)
    except TestException as e:
        assert e.message == sentinel.exception1
    else:
        assert False
        
    try:
        mock_fn(sentinel.arg1)
    except TestException as e:
        assert e.message == ""
    else:
        assert False
        
    try:
        mock_fn(sentinel.arg1)
    except TestException as e:
        assert e.message == sentinel.exception3
    else:
        assert False

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