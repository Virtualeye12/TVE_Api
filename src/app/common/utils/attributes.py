from __future__ import unicode_literals

try:
    import collections.abc as collections_abc  # only works on python 3.3+
except ImportError:
    import collections as collections_abc
from six import iteritems

def _wrap(val, obj_wrapper=None):
    if isinstance(val, collections_abc.Mapping):
        return AttrDict(val) if obj_wrapper is None else obj_wrapper(val)
    if isinstance(val, list):
        return AttrList(val)
    return val

class AttrList(object):
    def __init__(self, l, obj_wrapper=None):
        # make iterables into lists
        if not isinstance(l, list):
            l = list(l)
        self._l_ = l
        self._obj_wrapper = obj_wrapper

    def __repr__(self):
        return repr(self._l_)

    def __eq__(self, other):
        if isinstance(other, AttrList):
            return other._l_ == self._l_
        # make sure we still equal to a dict with the same data
        return other == self._l_

    def __ne__(self, other):
        return not self == other

    def __getitem__(self, k):
        l = self._l_[k]
        if isinstance(k, slice):
            return AttrList(l, obj_wrapper=self._obj_wrapper)
        return _wrap(l, self._obj_wrapper)

    def __setitem__(self, k, value):
        self._l_[k] = value

    def __iter__(self):
        return map(lambda i: _wrap(i, self._obj_wrapper), self._l_)

    def __len__(self):
        return len(self._l_)

    def __nonzero__(self):
        return bool(self._l_)
    __bool__ = __nonzero__

    def __getattr__(self, name):
        return getattr(self._l_, name)

    def __getstate__(self):
        return self._l_, self._obj_wrapper

    def __setstate__(self, state):
        self._l_, self._obj_wrapper = state


class AttrDict(object):
    """
    Helper class to provide attribute like access (read and write) to
    dictionaries. Used to provide a convenient way to access both results and
    nested dsl dicts.
    """
    def __init__(self, d):
        # assign the inner dict manually to prevent __setattr__ from firing
        super(AttrDict, self).__setattr__('_d_', d)

    def __contains__(self, key):
        return key in self._d_

    def __nonzero__(self):
        return bool(self._d_)
    __bool__ = __nonzero__

    def __dir__(self):
        # introspection for auto-complete in IPython etc
        return list(self._d_.keys())

    def __eq__(self, other):
        if isinstance(other, AttrDict):
            return other._d_ == self._d_
        # make sure we still equal to a dict with the same data
        return other == self._d_

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        r = repr(self._d_)
        if len(r) > 60:
            r = r[:60] + '...}'
        return r

    def __getstate__(self):
        return self._d_,

    def __setstate__(self, state):
        super(AttrDict, self).__setattr__('_d_', state[0])

    def __getattr__(self, attr_name):
        try:
            return self.__getitem__(attr_name)
        except KeyError:
            raise AttributeError(
                '{!r} object has no attribute {!r}'.format(self.__class__.__name__, attr_name))

    def __delattr__(self, attr_name):
        try:
            del self._d_[attr_name]
        except KeyError:
            raise AttributeError(
                '{!r} object has no attribute {!r}'.format(self.__class__.__name__, attr_name))

    def __getitem__(self, key):
        return _wrap(self._d_[key])

    def __setitem__(self, key, value):
        self._d_[key] = value

    def __delitem__(self, key):
        del self._d_[key]

    def __setattr__(self, name, value):
        if name in self._d_ or not hasattr(self.__class__, name):
            self._d_[name] = value
        else:
            # there is an attribute on the class (could be property, ..) - don't add it as field
            super(AttrDict, self).__setattr__(name, value)

    def __iter__(self):
        return iter(self._d_)

    def to_dict(self):
        return self._d_


def merge(data, new_data, raise_on_conflict=False):
    if not (isinstance(data, (AttrDict, collections_abc.Mapping))
            and isinstance(new_data, (AttrDict, collections_abc.Mapping))):
        raise ValueError('You can only merge two dicts! Got {!r} and {!r} instead.'.format(data, new_data))

    for key, value in iteritems(new_data):
        if key in data and isinstance(data[key], (AttrDict, collections_abc.Mapping)) and \
                isinstance(value, (AttrDict, collections_abc.Mapping)):
            merge(data[key], value, raise_on_conflict)
        elif key in data and data[key] != value and raise_on_conflict:
            raise ValueError('Incompatible data for key %r, cannot be merged.' % key)
        else:
            data[key] = value