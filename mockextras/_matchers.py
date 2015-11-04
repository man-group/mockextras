# mockextras.matchers
# Matchers and Stubs for mock.
# Copyright (C) 2012-2015 Man AHL
# E-mail: ManAHLTech AT ahl DOT com

# mockextras 1.0.0
# https://github.com/manahl/mockextras

# Released subject to the BSD License
# Please see https://github.com/manahl/mockextras/blob/master/LICENSE.txt

__all__ = ['Any', 'Contains', 'AnyOf']


class Any(object):
    """Matchers act as wildcards when defining a stub or when asserting call arguments.
    
    The Any matcher will match any object. 
    
    >>> whatever = Any()
    >>> assert whatever == 'hello'
    >>> assert whatever ==  100
    >>> assert whatever ==  range(10)
    
    You can optionally specify a type so that Any only matches objects of that type.
    
    >>> anystring = Any(basestring)
    >>> assert anystring == 'hello'
    >>> assert anystring == 'monkey'
    >>> assert anystring == u'bonjour'
    >>> assert anystring != ['hello', 'world']
    
    Any can be used when specifying stubs:
    
    >>> try:
    ...     from unittest.mock Mock, call
    ... except ImportError:
    ...     from mock import Mock, call
    >>>
    >>> from mockextras import stub
    >>> mock = Mock()
    >>> mock.side_effect = stub((call("hello", "world"), 100),
    ...                         (call("bye bye", Any()), 200))
    >>> mock("bye bye", "world")
    200
    >>> mock("bye bye", "Fred")
    200
    >>> mock("bye bye", range(100))
    200
    >>> mock("bye bye", { 'a' : 1000, 'b' : 2000})
    200
    
    or when asserting call arguments:
    
    >>> try:
    ...     from unittest.mock Mock
    ... except ImportError:
    ...     from mock import Mock
    >>>
    >>> mock = Mock()
    >>> mock("bye bye", "world")
    <Mock name='mock()' id='...'>
    >>> mock.assert_called_once_with("bye bye", Any())
    
    >>> mock("bye bye", "Fred")
    <Mock name='mock()' id='...'>
    >>> assert mock.call_args_list == [call("bye bye", "world"),
    ...                                call("bye bye", Any())]
    """
    def __init__(self, cls=object):
        self._cls = cls

    def __eq__(self, other):
        return isinstance(other, self._cls)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'Any(%s)' % ('' if self._cls is object else self._cls)


class Contains(object):
    """Matchers act as wildcards when defining a stub or when asserting call arguments.
    
    The Contains matcher will match objects that contain the given value or substring.
    
    >>> contains_five = Contains(5)
    >>> assert contains_five == range(10)
    >>> assert contains_five != range(4)

    >>> contains_ello = Contains('ello')
    >>> assert contains_ello == "hello"
    >>> assert contains_ello != "bye bye"

    Contains can be used when specifying stubs:
    
    >>> try:
    ...     from unittest.mock Mock, call
    ... except ImportError:
    ...     from mock import Mock, call
    >>>
    >>> from mockextras import stub
    >>> mock = Mock()
    >>> mock.side_effect = stub((call("hello", "world"), 100),
    ...                         (call("bye bye", Contains('monkey')), 200))
    >>> mock("bye bye", "uncle monkey")
    200
    
    or when asserting call arguments:
    
    >>> try:
    ...     from unittest.mock Mock
    ... except ImportError:
    ...     from mock import Mock
    >>>
    >>> mock = Mock()
    >>> mock("bye bye", "world")
    <Mock name='mock()' id='...'>
    >>> mock.assert_called_once_with("bye bye", Contains('or'))
    
    >>> mock("bye bye", "Fred")
    <Mock name='mock()' id='...'>
    >>> assert mock.call_args_list == [call("bye bye", "world"),
    ...                                call("bye bye", Contains('red'))]
    """
    def __init__(self, value):
        self._value = value

    def __eq__(self, other):
        return self._value in other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'Contains(%r)' % self._value


class AnyOf(object):
    """Matchers act as wildcards when defining a stub or when asserting call arguments.
    
    The AnyOf matcher will ....
    
    >>> is_a_small_prime = AnyOf(2,3,5,7,11,13)
    >>> assert is_a_small_prime == 3
    >>> assert is_a_small_prime != 4

    AnyOf can be used when specifying stubs:
    
    >>> try:
    ...     from unittest.mock Mock, call
    ... except ImportError:
    ...     from mock import Mock, call
    >>>
    >>> from mockextras import stub
    >>> mock = Mock()
    >>> mock.side_effect = stub((call("hello"), 100),
    ...                         (call(AnyOf('monkey', 'donkey', 'badger')), 200))
    >>> mock("monkey")
    200
    
    or when asserting call arguments:
    
    >>> try:
    ...     from unittest.mock Mock
    ... except ImportError:
    ...     from mock import Mock
    >>>
    >>> mock = Mock()
    >>> mock("donkey")
    <Mock name='mock()' id='...'>
    >>> mock.assert_called_once_with(AnyOf('monkey', 'donkey', 'badger'))
    
    >>> mock("monkey")
    <Mock name='mock()' id='...'>
    >>> assert mock.call_args_list == [call("donkey"),
    ...                                call(AnyOf('monkey', 'donkey', 'badger'))]
    """
    def __init__(self, *args):
        self._set = set(args)

    def __eq__(self, other):
        return other in self._set

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'AnyOf(%s)' % ', '.join(map(repr, self._set))
