from mockextras.stub import stub, seq, _Sequence, stub2
from mock import Mock, sentinel, patch, call
import pytest


def test_seq_empty():
    nxt = seq()
    with pytest.raises(StopIteration):
        nxt()


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


def test_seq():
    nxt = seq(sentinel.val1, sentinel.val2, sentinel.val3)
    assert nxt() == sentinel.val1
    assert nxt() == sentinel.val2
    assert nxt() == sentinel.val3
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
    nxt = seq(sentinel.val1, RuntimeError, RuntimeError(sentinel.val2), sentinel.val3)
    assert nxt() == sentinel.val1
    
    with pytest.raises(RuntimeError):
        nxt()
        
    try:
        nxt()
    except RuntimeError as e:
        assert e.message == sentinel.val2
    else:
        assert False
        
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
        with patch("mockextras.stub.call") as mock_callargs:
            assert mock_lookup.return_value == st(sentinel.arg1, sentinel.arg2)
    
    mock_callargs.assert_called_once_with(sentinel.arg1, sentinel.arg2)
    mock_lookup.assert_called_once_with(mock_callargs.return_value)


def test_stub_exception():
    st = stub()
    
    with patch.object(st, "_lookup", return_value=RuntimeError) as mock_lookup: #@UndefinedVariable
        with patch("mockextras.stub.call") as mock_callargs:
            with pytest.raises(RuntimeError):
                st(sentinel.arg1, sentinel.arg2)
    
    mock_callargs.assert_called_once_with(sentinel.arg1, sentinel.arg2)
    mock_lookup.assert_called_once_with(mock_callargs.return_value)


def test_stub_sequence():
    st = stub()
    
    with patch.object(st, "_lookup") as mock_lookup: #@UndefinedVariable
        with patch("mockextras.stub.call") as mock_callargs:
            with patch("mockextras.stub.isinstance", create=True, return_value=True) as mock_isinstance:
                assert mock_lookup.return_value.return_value == st(sentinel.arg1, sentinel.arg2)
    
    mock_isinstance.assert_called_once_with(mock_lookup.return_value, _Sequence)
    mock_callargs.assert_called_once_with(sentinel.arg1, sentinel.arg2)
    mock_lookup.assert_called_once_with(mock_callargs.return_value)
    mock_lookup.return_value.assert_called_once_with()


def test_stub_missing_case():
    st = stub()
    
    with patch.object(st, "_lookup", side_effect=KeyError) as mock_lookup: #@UndefinedVariableF
        with patch("mockextras.stub.call") as mock_callargs:
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
        
    try:
        mock_fn(sentinel.whatever, sentinel.argboom)
    except RuntimeError as e:
        assert e.message == sentinel.boom
    else:
        assert False
        
        
def test_stub_sequence_of_results():
    mock_fn = Mock()
    mock_fn.side_effect = stub((call(sentinel.argfoo), seq(sentinel.foo,
                                                           sentinel.bar,
                                                           RuntimeError,
                                                           RuntimeError(sentinel.boom),
                                                           sentinel.all_ok_now)))
    
    assert mock_fn(sentinel.argfoo) == sentinel.foo
    
    assert mock_fn(sentinel.argfoo) == sentinel.bar
    
    with pytest.raises(RuntimeError):
        mock_fn(sentinel.argfoo)
        
    try:
        mock_fn(sentinel.argfoo)
    except RuntimeError as e:
        assert e.message == sentinel.boom
    else:
        assert False
        
    assert mock_fn(sentinel.argfoo) == sentinel.all_ok_now
    
    with pytest.raises(StopIteration):
        mock_fn(sentinel.argfoo)
        

def test_stub2_no_args():
    with patch("mockextras.stub._Stub") as mock_stub:
        stub2()
    mock_stub.assert_called_once_with()        


def test_stub2_errors():
    with pytest.raises(RuntimeError):
        stub2(call())
    
    with pytest.raises(RuntimeError):
        stub2(sentinel.call, sentinel.value)

    with pytest.raises(RuntimeError):
        stub2(call(sentinel.a), sentinel.value, call(sentinel.b))
    
    with pytest.raises(RuntimeError):
        stub2(sentinel.call, sentinel.value)
    
    with pytest.raises(RuntimeError):
        stub2(sentinel.call1, sentinel.value1, sentinel.call2, sentinel.value2)
    
    with pytest.raises(RuntimeError):
        stub2(sentinel.call, sentinel.value)
    
    with pytest.raises(RuntimeError):
        stub2(sentinel.call1, sentinel.value1, sentinel.call2, sentinel.value2)
    
    with pytest.raises(RuntimeError):
        stub2(sentinel.value, call(sentinel.a, sentinel.b))
    
    with pytest.raises(RuntimeError):
        stub2(call(sentinel.a), call(sentinel.b), call(sentinel.c, sentinel.value))


def test_stub2_good_args():
    with patch("mockextras.stub._Stub") as mock_stub:
        stub2(call(sentinel.a, sentinel.b), sentinel.value)
    mock_stub.assert_called_once_with((call(sentinel.a, sentinel.b), sentinel.value))

    with patch("mockextras.stub._Stub") as mock_stub:
        stub2(call(sentinel.a), sentinel.value1, call(sentinel.b), sentinel.value1)
    mock_stub.assert_called_once_with((call(sentinel.a), sentinel.value1),
                                      (call(sentinel.b), sentinel.value1))