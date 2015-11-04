# mockextras.fluent
# Matchers and Stubs for mock.
# Copyright (C) 2012-2015 Man AHL
# E-mail: ManAHLTech AT ahl DOT com

# mockextras 1.0.0
# https://github.com/manahl/mockextras

# Released subject to the BSD License
# Please see https://github.com/manahl/mockextras/blob/master/LICENSE.txt

from ._matchers import __all__ as matchers_all
from ._stub import _Sequence, _Stub
try:
    from unittest.mock import call, _is_exception, _is_instance_mock
except ImportError:
    try:
        from mock.mock import call, _is_exception, _is_instance_mock
    except ImportError:
        from mock import call, _is_exception, _is_instance_mock
from os import linesep


__all__ = ['when']


def when(mock_fn):
    class ListSeq(_Sequence):
        def __init__(self):
            self.list = []

        def __call__(self):
            if len(self.list) > 1:
                retval = self.list.pop(0)
            else:
                retval = self.list[0]
            if _is_exception(retval):
                raise retval
            return retval

    class When(object):
        def __init__(self, mock_fn):
            self._mock_fn = mock_fn
            if not _is_instance_mock(self._mock_fn):
                raise RuntimeError("mock_fn must be an instance of Mock")

            if not isinstance(self._mock_fn.side_effect, _Stub):
                if self._mock_fn.side_effect is not None:
                    raise RuntimeError("Mock '%s' already has a side_effect set defined" % self._mock_fn)

                self._mock_fn.side_effect = _Stub()

            if not isinstance(self._mock_fn.side_effect._results, list):  #pylint: disable=protected-access
                self._mock_fn.side_effect._results = list(self._mock_fn.side_effect._results)  #pylint: disable=protected-access

        def called_with(self, *args, **kwargs):
            return CalledWith(self._mock_fn.side_effect._results, call(*args, **kwargs))  #pylint: disable=protected-access

    class CalledWith(object):
        def __init__(self, results, key):
            self._results = results
            self._key = key
            self._list = None

        def then(self, obj):
            if self._list is None:
                s = ListSeq()
                self._results.append((self._key, s))
                self._list = s.list
            self._list.append(obj)
            return self

        def __repr__(self):
            return ""

    return When(mock_fn)


when.__doc__ = """Provides a fluent API for specifying stubs.

For example, you can specify different values to return or exceptions to raise based on the arguments
passed into the called_with:

>>> try:
...     from unittest.mock Mock
... except ImportError:
...     from mock import Mock
>>>
>>> mock = Mock()
>>> when(mock).called_with("hello").then("world")
<BLANKLINE>
>>> when(mock).called_with("foo").then("bar")
<BLANKLINE>
>>> when(mock).called_with(100, 200).then(RuntimeError("Boom!"))
<BLANKLINE>
>>> mock("hello")
'world'
>>> mock("foo")
'bar'
>>> mock(100, 200)
Traceback (most recent call last):
...
RuntimeError: Boom!


You can use 'then' multiple times to specify a sequence of results.

>>> mock = Mock()
>>> when(mock).called_with("monkey").then("weezel")\\
...                                 .then("badger")\\
...                                 .then(RuntimeError("Boom!"))
<BLANKLINE>
>>> mock("monkey")
'weezel'
>>> mock("monkey")
'badger'
>>> mock("monkey")
Traceback (most recent call last):
...
RuntimeError: Boom!

The last value is repeated for any subsequent calls.

You can use matchers, such as Any(), as wild-card arguments when matching call arguments. The stub's
configuration is searched in the order it was specified so you can put more specific call argument
specifications ahead of more general ones. For example:

>>> from mockextras import Any
>>> mock = Mock()
>>> when(mock).called_with(100, 200).then("monkey")
<BLANKLINE>
>>> when(mock).called_with(100, Any()).then("hello")
<BLANKLINE>
>>> mock(100, 200)
'monkey'
>>> mock(100, 300)
'hello'
>>> mock(100, "monkey")
'hello'
>>> mock(100, { "key" : 1000 })
'hello'

The following matchers are available in mockextras:
%s

See their documentation for more info.
""" % linesep.join('  * %s' % m for m in matchers_all)
