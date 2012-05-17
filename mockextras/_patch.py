import mock
from functools import wraps


__all__ = ["patch"]


class patch(object):
    def __init__(self, *patch_args, **patch_kwargs):
        self.patch = mock.patch(*patch_args, **patch_kwargs)

    def __call__(self, func):
        if isinstance(func, mock.ClassTypes):
            return self.patch(func)
        else:
            @wraps(func)
            def patched(*args, **kwargs):
                with self.patch as mock:
                    return func(mock, *args, **kwargs)
            return patched

    def __enter__(self):
        return self.patch.__enter__()

    def __exit__(self, *args):
        return self.patch.__exit__(*args)


class _patch_object(patch):
    def __init__(self, *patch_args, **patch_kwargs):
        self.patch = mock.patch.object(*patch_args, **patch_kwargs)


patch.object = _patch_object
