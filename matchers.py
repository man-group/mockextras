class Any(object):
    def __init__(self, cls=object):
        self._cls = cls
    
    def __eq__(self, other):
        return isinstance(other, self._cls)

    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __repr__(self):
        return 'Any(%s)' % ('' if self._cls is object else self._cls)
    
    
class Contains(object):
    def __init__(self, value):
        self._value = value
    
    def __eq__(self, other):
        return self._value in other

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        return 'Contains(%r)' % self._value