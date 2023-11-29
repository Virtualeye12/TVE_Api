from collections import OrderedDict
import json

class LimitedSizeDict(OrderedDict):
    def __init__(self, *args, **kwds):
        if "size_limit" not in kwds:
            raise ValueError("'size_limit' must be passed as a keyword "
                             "argument")
        self.size_limit = kwds.pop("size_limit")
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        if len(args) == 1 and len(args[0]) + len(kwds) > self.size_limit:
            raise ValueError("Tried to initialize LimitedSizedDict with more "
                             "value than permitted with 'limit_size'")
        super(LimitedSizeDict, self).__init__(*args, **kwds)

    def __setitem__(self, key, value, dict_setitem=OrderedDict.__setitem__):
        dict_setitem(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)

    def __eq__(self, other):
        if self.size_limit != other.size_limit:
            return False
        return super(LimitedSizeDict, self).__eq__(other)


class UnupdatableDict(dict):
    def __setitem__(self, key, value):
        if key in self:
            raise KeyError("Can't update key '%s'" % key)
        super(UnupdatableDict, self).__setitem__(key, value)\


def merge_dict(base, delta):
    for k, dv in delta.items():
        bv = base.get(k)
        if isinstance(dv, dict) and isinstance(bv, dict):
            merge_dict(bv, dv)
        else:
            base[k] = dv


def load_commented_json(filename):
    with open(filename) as f:
        contents = f.read()

    return json.loads(uncomment_json(contents))


def uncomment_json(commented_json_str):
    lines = commented_json_str.splitlines()
    nocomment = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("//") or stripped.startswith("#"):
            continue
        nocomment.append(line)

    return " ".join(nocomment)



try:
    import funcsigs as inspect
except ImportError:
    import inspect

from future.utils import iteritems

KEYWORD_KINDS = {inspect.Parameter.POSITIONAL_OR_KEYWORD,
                 inspect.Parameter.KEYWORD_ONLY}


class FromDict(object):
    @classmethod
    def from_dict(cls, dict):
        if dict is None:
            return cls()
        params = inspect.signature(cls.__init__).parameters

        if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in
               params.values()):
            return cls(**dict)

        param_names = set()
        for i, (name, param) in enumerate(iteritems(params)):
            if i == 0 and name == "self":
                continue
            if param.kind in KEYWORD_KINDS:
                param_names.add(name)
        filtered_dict = {k: v for k, v in iteritems(dict) if k in param_names}
        return cls(**filtered_dict)