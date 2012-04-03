from mock import _is_exception, call, _Call


__all__ = ['seq', 'stub']
    
    
class _Sequence(object):
    def __init__(self, *args):
        if len(args) != 1:
            self._iterator = iter(args)
        else:
            self._iterator = iter(args[0])
        
    def __call__(self):
        retval = next(self._iterator)
        if _is_exception(retval):
            raise retval
        return retval


def seq(*args):
    """Used in conjunction with stub to define a sequence of return values for a stub
    
    You can pass in several arguments:
    
    >>> mock = Mock(side_effect = stub2(call(), seq(1,2,3)))
    >>> mock()
    1
    >>> mock()
    2
    >>> mock()
    3
    
    or a single iterable argument, for example a list:
    
    >>> l = range(5)
    >>> mock = Mock(side_effect = stub2(call(), seq(l)))
    >>> mock()
    1
    >>> mock()
    2
    >>> mock()
    3

    or a iterator/generator:

    >>> i = xrange(5)
    >>> mock = Mock(side_effect = stub2(call(), seq(i)))
    >>> mock()
    1
    >>> mock()
    2
    >>> mock()
    3
    """
    return _Sequence(*args)


class _Stub(object):
    def __init__(self, *args):
        self._results = args

    def _lookup(self, k):
        for key, value in self._results:
            if key == k:
                return value
        raise KeyError(k)
    
    def __call__(self, *args, **kwargs):
        obj = self._lookup(call(*args, **kwargs))
        if _is_exception(obj):
            raise obj
        if isinstance(obj, _Sequence):
            return obj()
        return obj


def stub(*args):
    """Creates a stub function that can be used as the side_effect of a mock.
    The stub is configured so it returns different values depending on the
    arguments passed to it:
    
    >>> from mock import Mock
    >>> mock = Mock()
    >>> mock.side_effect = stub((call("hello"), "world"),
    ...                         (call("foo"),   "bar"))
    >>> mock("hello")
    'world'
    >>> mock("foo")
    'bar'
    
    or you can specify an exception to raise:
    
    >>> from mock import Mock
    >>> mock = Mock()
    >>> mock.side_effect = stub((call("hello"),   "world"),
    ...                         (call("bye bye"), ValueError),
    ...                         (call("foo"),     IndexError('foo')))
    >>> mock("bye bye")
    Traceback (most recent call last):
    ...
    ValueError
    >>> mock("foo")
    Traceback (most recent call last):
    ...
    IndexError: foo
    
    You can use seq to specify a sequence of return values, for example:
    
    >>> from mock import Mock
    >>> mock = Mock()
    >>> mock.side_effect = stub((call("hello"), seq("street", "world", "universe")))
    >>> mock("hello")
    'street'
    >>> mock("hello")
    'world'
    >>> mock("hello")
    'universe'
    
    See seq for more info.
    
    You can use matchers to wildcard arguments when matching calls arguments for example 'Any':
    
    >>> from matchers import Any
    >>> mockn = Mock()
    >>> mock.side_effect = stub((call(100, Any()), "hello"))
    >>> mock(100, "monkey")
    'hello'
    >>> mock(100, { "key" : 1000 })
    'hello'
    
    See the matchers module for more info.
    """
    return _Stub(*args)


def stub2(*args):
    """Creates a stub function that can be used as the side_effect of a mock.
    The stub is configured so it returns different values depending on the
    arguments passed to it:
    
    >>> from mock import Mock
    >>> mock = Mock()
    >>> mock.side_effect = stub2(call("hello"), "world",
    ...                          call("foo"),   "bar")
    >>> mock("hello")
    'world'
    >>> mock("foo")
    'bar'
    
    or you can specify an exception to raise:
    
    >>> from mock import Mock
    >>> mock = Mock()
    >>> mock.side_effect = stub2(call("hello"),   "world",
    ...                          call("bye bye"), ValueError,
    ...                          call("foo"),     IndexError('foo'))
    >>> mock("bye bye")
    Traceback (most recent call last):
    ...
    ValueError
    >>> mock("foo")
    Traceback (most recent call last):
    ...
    IndexError: foo
    
    You can use seq to specify a sequence of return values, for example:
    
    >>> from mock import Mock
    >>> mock = Mock()
    >>> mock.side_effect = stub2(call("hello"), seq("street", "world", "universe"))
    >>> mock("hello")
    'street'
    >>> mock("hello")
    'world'
    >>> mock("hello")
    'universe'
    
    See seq for more info.
    
    You can use matchers to wildcard arguments when matching calls arguments for example 'Any':
    
    >>> from matchers import Any
    >>> mock = Mock()
    >>> mock.side_effect = stub2(call(100, Any()), "hello")
    >>> mock(100, "monkey")
    'hello'
    >>> mock(100, { "key" : 1000 })
    'hello'
    
    See the matchers module for more info.
    """ 
    if len(args) % 2 > 0:
        raise RuntimeError('Expected arguments in the form call,result,call,result...')
    args = zip(args[::2], args[1::2])
    if not all(isinstance(cll, _Call) and not isinstance(rslt, _Call) for cll, rslt in args):
        raise RuntimeError('Expected arguments in the form call,result,call,result...')
    return _Stub(*args)
