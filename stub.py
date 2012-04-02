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
    return _Stub(*args)


def stub2(*args):
    if len(args) % 2 > 0:
        raise RuntimeError('Expected arguments in the form call,result,call,result...')
    args = zip(args[::2], args[1::2])
    if not all(isinstance(cll, _Call) and not isinstance(rslt, _Call) for cll, rslt in args):
        raise RuntimeError('Expected arguments in the form call,result,call,result...')
    return _Stub(*zip(args[::2], args[1::2]))