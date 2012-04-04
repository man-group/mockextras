# mockextras.stub
# Matchers and Stubs for mock.
# Copyright (C) 2012 Andrew Burrows
# E-mail: burrowsa AT gmail DOT com

# mockextras 0.0.0
# https://github.com/burrowsa/mockextras

# Released subject to the BSD License
# Please see https://github.com/burrowsa/mockextras/blob/master/LICENSE.txtfrom mock import _is_exception, call, _Call


"""mockextras.stub provides an implementation of stubs that can be used with mock.
The you stub a mock by setting its side_effect:

>>> from mock import Mock, call
>>> mock = Mock()
>>> mock.side_effect = stub((call("hello"), "world"),
...                         (call("foo"),   1,2,4,8),
...                         (call("bar"),   seq(xrange(100))))
>>> mock("hello")
'world'
>>> mock("foo")
1
>>> mock("foo")
2
>>> mock("foo")
4

See stub() and seq() for more info.
"""


from mock import _is_exception, call


__all__ = ['seq', 'stub']
    
    
class _Sequence(object):
    def __init__(self, iterable):
        self._iterator = iter(iterable)
        
    def __call__(self):
        retval = next(self._iterator)
        if _is_exception(retval):
            raise retval
        return retval


def seq(iterable):
    """Used in conjunction with stub to define a sequence of return values for a stub
    based on an iterable, such as a container:
    
    >>> from mock import Mock, call 
    >>> l = range(1, 5)
    >>> mock = Mock(side_effect = stub((call(), seq(l))))
    >>> mock()
    1
    >>> mock()
    2
    >>> mock()
    3

    or a generator:

    >>> i = xrange(1, 5)
    >>> mock = Mock(side_effect = stub((call(), seq(i))))
    >>> mock()
    1
    >>> mock()
    2
    >>> mock()
    3
    """
    return _Sequence(iterable)


class _Stub(object):
    def __init__(self, *args):
        self._results = tuple( (conf[0], seq(conf[1:])) if len(conf) > 2 else conf for conf in args )

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
    
    >>> from mock import Mock, call
    >>> mock = Mock()
    >>> mock.side_effect = stub((call("hello"), "world"),
    ...                         (call("foo"),   "bar"))
    >>> mock("hello")
    'world'
    >>> mock("foo")
    'bar'
    
    or you can specify an exception to raise:
    
    >>> from mock import Mock, call
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

    You can specify a sequence of return values, for example:
    
    >>> from mock import Mock, call
    >>> mock = Mock()
    >>> mock.side_effect = stub((call("hello"), "street", "world", "universe"))
    >>> mock("hello")
    'street'
    >>> mock("hello")
    'world'
    >>> mock("hello")
    'universe'
    
    You can use seq() to specify a sequence of return values based on an iterable, for example:
    
    >>> from mock import Mock, call
    >>> mock = Mock()
    >>> mock.side_effect = stub((call("hello"), seq(xrange(100))))
    >>> mock("hello")
    0
    >>> mock("hello")
    1
    >>> mock("hello")
    2
    
    See seq() for more info.
    
    You can use matchers to wildcard arguments when matching calls arguments for example 'Any':
    
    >>> from matchers import Any
    >>> mockn = Mock()
    >>> mock.side_effect = stub((call(100, Any()), "hello"))
    >>> mock(100, "monkey")
    'hello'
    >>> mock(100, { "key" : 1000 })
    'hello'
    
    See mockextras.matchers for more info.
    """
    return _Stub(*args)