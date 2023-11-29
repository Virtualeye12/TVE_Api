from __future__ import unicode_literals

import importlib
import json
import numbers
import re
from builtins import bytes as newbytes, str as newstr
from datetime import datetime
from functools import wraps
from pathlib import Path
from future.utils import text_type


def unicode_string(string):
    if isinstance(string, text_type):
        return string
    if isinstance(string, bytes):
        return string.decode("utf8")
    if isinstance(string, newstr):
        return text_type(string)
    if isinstance(string, newbytes):
        string = bytes(string).decode("utf8")

    raise TypeError("Cannot convert %s into unicode string" % type(string))


def json_string(json_object, indent=2, sort_keys=True):
    json_dump = json.dumps(json_object, indent=indent, sort_keys=sort_keys,
                           separators=(',', ': '))
    return unicode_string(json_dump)


def batchify(it, batch_size=128):
    batch = []
    for item in it:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []

    if batch:
        yield batch

def flatten(lst):
    out = []
    for v in lst:
        if v is None:
            continue
        if isinstance(v, list):
            out.extend(flatten(v))
        else:
            out.append(v)
    return out
    