# coding: utf-8
"""
    sickle._compat
    ~~~~~~~~~~~~~~

    Python 2/3 compatibility layer

    :copyright: Copyright 2015 Mathias Loesch
"""

import sys

PY3 = sys.version_info >= (3, 0)

if PY3:  # pragma: no cover
    string_types = str,
    text_type = str
    binary_type = bytes
else:  # pragma: no cover
    string_types = basestring,
    text_type = unicode
    binary_type = str


def to_unicode(x):  # pragma: no cover
    """Convert argument into a unicode string."""
    if PY3:
        return str(x)
    else:
        return x.decode('utf-8')

def to_str(x):  # pragma: no cover
    """Convert unicode argument into a string."""
    if PY3:
        return str(x)
    else:
        return x.encode('utf-8')
