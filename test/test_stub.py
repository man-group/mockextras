from mockextras import stub, seq, Any
from mockextras._stub import _Sequence
try:
    from unittest.mock import Mock, sentinel, patch, call
except ImportError:
    from mock import Mock, sentinel, patch, call
import pytest
from datetime import datetime


def test_seq_empty_list():
    nxt = seq([])
    with pytest.raises(StopIteration):
        nxt()


def test_seq_empty_list_iterator():
    nxt = seq(iter([]))
    with pytest.raises(StopIteration):
        nxt()


def test_seq_empty_generator():
    nxt = seq(i for i in [])
    with pytest.raises(StopIteration):
        nxt()


def test_seq_list():
    nxt = seq([sentinel.val1, sentinel.val2, sentinel.val3])
    assert nxt() == sentinel.val1
    assert nxt() == sentinel.val2
    assert nxt() == sentinel.val3
    with pytest.raises(StopIteration):
        nxt()


def test_seq_list_iterator():
    nxt = seq(iter(iter([sentinel.val1, sentinel.val2, sentinel.val3])))
    assert nxt() == sentinel.val1
    assert nxt() == sentinel.val2
    assert nxt() == sentinel.val3
    with pytest.raises(StopIteration):
        nxt()


def test_seq_generator():
    nxt = seq(i for i in [sentinel.val1, sentinel.val2, sentinel.val3])
    assert nxt() == sentinel.val1
    assert nxt() == sentinel.val2
    assert nxt() == sentinel.val3
    with pytest.raises(StopIteration):
        nxt()


def test_seq_raises_exceptions():
    nxt = seq([sentinel.val1, RuntimeError, RuntimeError(sentinel.val2), sentinel.val3])
    assert nxt() == sentinel.val1

    with pytest.raises(RuntimeError):
        nxt()

    with pytest.raises(RuntimeError) as err:
        nxt()
    assert str(err.value) == str(sentinel.val2)

    assert nxt() == sentinel.val3

    with pytest.raises(StopIteration):
        nxt()


def test_lookup():
    with pytest.raises(KeyError):
        stub()._lookup(sentinel.keya)

    test_data = stub((sentinel.keya, sentinel.vala), (sentinel.keyb, sentinel.valb))

    assert sentinel.vala == test_data._lookup(sentinel.keya)

    assert sentinel.valb == test_data._lookup(sentinel.keyb)

    with pytest.raises(KeyError):
        test_data._lookup(sentinel.keyc)


def test_universal_side_effect():
    st = stub()

    with patch.object(st, "_lookup") as mock_lookup: #@UndefinedVariable
        with patch("mockextras._stub.call") as mock_callargs:
            assert mock_lookup.return_value == st(sentinel.arg1, sentinel.arg2)

    mock_callargs.assert_called_once_with(sentinel.arg1, sentinel.arg2)
    mock_lookup.assert_called_once_with(mock_callargs.return_value)


def test_stub_exception():
    st = stub()

    with patch.object(st, "_lookup", return_value=RuntimeError) as mock_lookup: #@UndefinedVariable
        with patch("mockextras._stub.call") as mock_callargs:
            with pytest.raises(RuntimeError):
                st(sentinel.arg1, sentinel.arg2)

    mock_callargs.assert_called_once_with(sentinel.arg1, sentinel.arg2)
    mock_lookup.assert_called_once_with(mock_callargs.return_value)


def test_stub_sequence():
    st = stub()

    with patch.object(st, "_lookup") as mock_lookup: #@UndefinedVariable
        with patch("mockextras._stub.call") as mock_callargs:
            with patch("mockextras._stub.isinstance", create=True, return_value=True) as mock_isinstance:
                assert mock_lookup.return_value.return_value == st(sentinel.arg1, sentinel.arg2)

    mock_isinstance.assert_called_once_with(mock_lookup.return_value, _Sequence)
    mock_callargs.assert_called_once_with(sentinel.arg1, sentinel.arg2)
    mock_lookup.assert_called_once_with(mock_callargs.return_value)
    mock_lookup.return_value.assert_called_once_with()


def test_stub_missing_case():
    st = stub()

    with patch.object(st, "_lookup", side_effect=KeyError) as mock_lookup: #@UndefinedVariableF
        with patch("mockextras._stub.call") as mock_callargs:
            with pytest.raises(KeyError):
                assert st(sentinel.arg1, sentinel.arg2)

    mock_callargs.assert_called_once_with(sentinel.arg1, sentinel.arg2)
    mock_lookup.assert_called_once_with(mock_callargs.return_value)


def test_stub_switches_on_args():
    mock_fn = Mock()
    mock_fn.side_effect = stub((call(sentinel.argfoo), sentinel.foo),
                               (call(sentinel.whatever, sentinel.argbar), sentinel.bar),
                               (call(sentinel.whatever, sentinel.argbang), RuntimeError),
                               (call(sentinel.whatever, sentinel.argboom), RuntimeError(sentinel.boom)))

    assert mock_fn(sentinel.argfoo) == sentinel.foo

    assert mock_fn(sentinel.whatever, sentinel.argbar) == sentinel.bar

    with pytest.raises(RuntimeError):
        mock_fn(sentinel.whatever, sentinel.argbang)

    with pytest.raises(RuntimeError) as err:
        mock_fn(sentinel.whatever, sentinel.argboom)
    assert str(err.value) == str(sentinel.boom)


def test_stub_sequence_of_results():
    mock_fn = Mock()
    mock_fn.side_effect = stub((call(sentinel.argfoo), sentinel.foo,
                                                       sentinel.bar,
                                                       RuntimeError,
                                                       RuntimeError(sentinel.boom),
                                                       sentinel.all_ok_now))

    assert mock_fn(sentinel.argfoo) == sentinel.foo

    assert mock_fn(sentinel.argfoo) == sentinel.bar

    with pytest.raises(RuntimeError):
        mock_fn(sentinel.argfoo)
        
    with pytest.raises(RuntimeError) as err:
        mock_fn(sentinel.argfoo)
    assert str(err.value) == str(sentinel.boom)

    assert mock_fn(sentinel.argfoo) == sentinel.all_ok_now

    with pytest.raises(StopIteration):
        mock_fn(sentinel.argfoo)


def test_stub_sequence_of_results_from_iterator():
    mock_fn = Mock()
    results = iter([sentinel.foo, sentinel.bar, RuntimeError, RuntimeError(sentinel.boom), sentinel.all_ok_now])
    mock_fn.side_effect = stub((call(sentinel.argfoo), seq(results)))

    assert mock_fn(sentinel.argfoo) == sentinel.foo

    assert mock_fn(sentinel.argfoo) == sentinel.bar

    with pytest.raises(RuntimeError):
        mock_fn(sentinel.argfoo)
        
    with pytest.raises(RuntimeError) as err:
        mock_fn(sentinel.argfoo)
    assert str(err.value) == str(sentinel.boom)

    assert mock_fn(sentinel.argfoo) == sentinel.all_ok_now

    with pytest.raises(StopIteration):
        mock_fn(sentinel.argfoo)


def test_stub_arg_matching():
    mock_fn = Mock()
    mock_fn.side_effect = stub((call(), sentinel.res0),
                               (call(sentinel.arg1), sentinel.res1),
                               (call(datetime(1978, 2, 2, 12, 34, 56)), sentinel.res2),
                               (call(Any()), sentinel.res3),
                               (call(x=sentinel.argx, y=sentinel.argy), sentinel.res4),
                               (call(x=sentinel.argx, y=datetime(1978, 2, 2, 12, 34, 56)), sentinel.res5),
                               (call(x=sentinel.argx, y=Any()), sentinel.res6))

    assert mock_fn() == sentinel.res0
    assert mock_fn(sentinel.arg1) == sentinel.res1
    assert mock_fn(Any()) == sentinel.res1
    assert mock_fn(Any(datetime)) == sentinel.res2
    assert mock_fn(datetime(1978, 2, 2, 12, 34, 56)) == sentinel.res2
    assert mock_fn(datetime(1978, 2, 2, 12, 45, 00)) == sentinel.res3
    assert mock_fn(sentinel.meh) == sentinel.res3
    assert mock_fn(x=sentinel.argx, y=sentinel.argy) == sentinel.res4
    assert mock_fn(x=sentinel.argx, y=datetime(1978, 2, 2, 12, 34, 56)) == sentinel.res5
    assert mock_fn(x=sentinel.argx, y=Any()) == sentinel.res4
    assert mock_fn(x=sentinel.argx, y=Any(datetime)) == sentinel.res5
    assert mock_fn(x=sentinel.argx, y=sentinel.meh) == sentinel.res6
