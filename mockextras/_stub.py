# mockextras.stub
# Matchers and Stubs for mock.
# Copyright (C) 2012-2015 Man AHL
# E-mail: ManAHLTech AT ahl DOT com

# mockextras 1.0.0
# https://github.com/manahl/mockextras

# Released subject to the BSD License
# Please see https://github.com/manahl/mockextras/blob/master/LICENSE.txt

from ._matchers import __all__ as matchers_all
try:
    from unittest.mock import _is_exception, call
except ImportError:
    try:
        from mock.mock import call, _is_exception 
    except ImportError:
        from mock import call, _is_exception
from os import linesep


__all__ = ['seq', 'stub', 'UnexpectedStubCall']


class _Sequence(object):
    def __init__(self, iterable):
        self._iterator = iter(iterable)

    def __call__(self):
        retval = next(self._iterator)
        if _is_exception(retval):
            raise retval
        return retval


def seq(iterable):
    """Used to define a sequence of return values for a stub based on an iterable, such as a container:
    
    >>> try:
    ...     from unittest.mock Mock, call
    ... except ImportError:
    ...     from mock import Mock, call
    >>>
    >>> l = range(1, 5)
    >>> fn = stub((call(), seq(l)))
    >>> fn()
    1
    >>> fn()
    2
    >>> fn()
    3

    or a generator:

    >>> i = xrange(1, 5)
    >>> fn = stub((call(), seq(i)))
    >>> fn()
    1
    >>> fn()
    2
    >>> fn()
    3
    """
    return _Sequence(iterable)


class UnexpectedStubCall(Exception):
    pass


def _one_per_line_indented(results, indent=4):
    return ("""
""" + " " * indent).join(str(k) for k, _ in results)


class _Stub(object):
    def __init__(self, *args):
        self._results = tuple((conf[0], seq(conf[1:])) if len(conf) > 2 else conf for conf in args)

    def _lookup(self, k):
        for key, value in self._results:
            # Some classes don't play by the rules so try the equals both ways around
            if key == k or k == key:
                return value
        if self._results:
            raise UnexpectedStubCall("""Unexpected stub call:
    %s
The following calls are configured:
    %s
""" % (k, _one_per_line_indented(self._results)))
        else:
            raise UnexpectedStubCall("Unexpected call of an unconfigured stub")

    def __call__(self, *args, **kwargs):
        obj = self._lookup(call(*args, **kwargs))
        if _is_exception(obj):
            raise obj
        if isinstance(obj, _Sequence):
            return obj()
        return obj


def stub(*args):
    return _Stub(*args)


stub.__doc__ = """Makes stubs that can be used stand-alone or with mock.

Stubs are dumb functions, used in testing, they do no processing but they can take arguments and return 
predefined results.

A stub is configured so it returns different values depending on the arguments passed to it. You configure
it with one or more pairs of call arguments and results then when the stub is called with a given set of call
arguments the corresponding result is returned. If the result is an Exception the result is raised. If more
than one result is specified the results will be returned/raised one at a time over successive calls to the
stub. If you wish to specify successive results using an iterable you must wrap it with seq().

You can use a stub in place of a function, for example:

>>> try:
...     from unittest.mock call
... except ImportError:
...     from mock import call
>>>
>>> fn = stub((call("hello"), "world"),
...           (call("foo"),   1, 2, 4, 8),
...           (call("bar"),   seq(xrange(100))),
...           (call("baz"),   KeyError('baz')),
...           (call("boom"),  100, RuntimeError, 200, ValueError("boom")))
>>> fn("hello")
'world'
>>> fn("foo")
1
>>> fn("foo")
2
>>> fn("foo")
4

Or you can combine it with a mock by setting it as the side_effect. This has the advantage that you can later
verify the function was called as expected.

>>> try:
...     from unittest.mock Mock, call
... except ImportError:
...     from mock import Mock, call
>>>
>>> mock = Mock()
>>> mock.side_effect = stub((call("hello"), "world"),
...                         (call("foo"),   1,2,4,8))
>>> mock("hello")
'world'
>>> mock("foo")
1
>>> mock("foo")
2
>>> mock("foo")
4
>>> assert mock.call_args_list == [call("hello"), call("foo"), call("foo"), call("foo")]

Also you can use stubs as methods on Mock objects. Whether you use them directly as the methods or as the
side_effect of a mock method depends on whether you want to verify the method calls.

>>> mock_obj = Mock(my_first_method=stub((call(50), 100), (call(100), 200)))
>>> mock_obj.my_second_method = stub((call("a"), "aa"), (call("b"), "bb"))
>>> mock_obj.my_third_method.side_effect = stub((call(123), 456), (call(789), 54321))

>>> mock_obj.my_first_method(50)
100
>>> mock_obj.my_second_method('b')
'bb'
>>> mock_obj.my_third_method(123)
456
>>> assert mock_obj.mock_calls == [call.my_third_method(123)] # only the mocked call is recorded

You can use matchers, such as Any(), as wild-card arguments when matching call arguments. The stub's
configuration is searched in the order it was specified so you can put more specific call argument
specifications ahead of more general ones.

For example:

>>> from mockextras import Any
>>> fn = stub((call(100, 200),   "monkey"),
...           (call(100, Any()), "hello"))
>>> fn(100, 200)
'monkey'
>>> fn(100, 300)
'hello'
>>> fn(100, "monkey")
'hello'
>>> fn(100, { "key" : 1000 })
'hello'

The following matchers are available in mockextras:
%s

See their documentation for more info.
""" % linesep.join('  * %s' % m for m in matchers_all)
