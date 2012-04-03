from mock import Mock, _is_exception, call
from .stub import _Sequence, _Stub


def when(mock_fn):
    """Provides a fluent API for specifying mock side_effects.
    
    For example, you can specify different values to return or exceptions to raise 
    based on the arguments passed into the called_with:
        
    >>> mock_fn = Mock()
    >>> when(mock_fn).called_with("hello").then("world")
    <BLANKLINE>
    >>> when(mock_fn).called_with("foo").then("bar")
    <BLANKLINE>
    >>> when(mock_fn).called_with(100, 200).then(RuntimeError("Boom!"))
    <BLANKLINE>
    >>> mock_fn("hello")
    'world'
    >>> mock_fn("foo")
    'bar'
    >>> mock_fn(100, 200)
    Traceback (most recent call last):
    ...
    RuntimeError: Boom!


    You can use 'then' multiple times to specify a sequence of side effects.
    
    >>> mock_fn = Mock()
    >>> when(mock_fn).called_with("monkey").then("weezel")\\
    ...                                    .then("badger")\\
    ...                                    .then(RuntimeError("Boom!"))
    <BLANKLINE>
    >>> mock_fn("monkey")
    'weezel'
    >>> mock_fn("monkey")
    'badger'
    >>> mock_fn("monkey")
    Traceback (most recent call last):
    ...
    RuntimeError: Boom!
    
    The last value is repeated for any subsequent calls.
    
    You can use matchers to wildcard arguments when matching calls arguments for example 'Any':
    
    >>> from matchers import Any
    >>> mock_fn = Mock()
    >>> when(mock_fn).called_with(100, Any()).then("hello")
    <BLANKLINE>
    >>> mock_fn(100, "monkey")
    'hello'
    >>> mock_fn(100, { "key" : 1000 })
    'hello'
    
    See the matchers module for more info.
    """
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
            if not isinstance(self._mock_fn, Mock):
                raise RuntimeError("mock_fn must be an instance of Mock")
            
            if not isinstance(self._mock_fn.side_effect, _Stub):
                if self._mock_fn.side_effect is not None:
                    raise RuntimeError("Mock '%s' already has a side_effect set defined" % self._mock_fn)
                
                self._mock_fn.side_effect = _Stub()
            
            if not isinstance(self._mock_fn.side_effect._results, list):
                self._mock_fn.side_effect._results = list(self._mock_fn.side_effect._results)
        
        def called_with(self, *args, **kwargs):
            return CalledWith(self._mock_fn.side_effect._results, call(*args, **kwargs))
    
    class CalledWith(object):
        def __init__(self, results, key):
            self._results = results
            self._key = key
    
        def then(self, obj):
            self._setdefault(self._key, ListSeq()).list.append(obj)
            return self
    
        def __repr__(self):
            return ""
        
        def _setdefault(self, k, default):
            for key, value in self._results:
                if key == k:
                    return value
            self._results.append((k, default))
            return default
    
    return When(mock_fn)