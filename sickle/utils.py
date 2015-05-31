# coding: utf-8
"""
    sickle.utils
    ~~~~~~~~~~~~

    Collects utility functions.

    :copyright: Copyright 2015 Mathias Loesch
"""

import re
from collections import defaultdict


def get_namespace(element):
    """Return the namespace of an XML element.

    :param element: An XML element.
    """
    return re.search('(\{.*\})', element.tag).group(1)


def xml_to_dict(tree, paths=None, nsmap=None, strip_ns=False):
    """Convert an XML tree to a dictionary.

    :param tree: etree Element
    :type tree: :class:`lxml.etree._Element`
    :param paths: An optional list of XPath expressions applied on the XML tree.
    :type paths: list[basestring]
    :param nsmap: An optional prefix-namespace mapping for conciser spec of paths.
    :type nsmap: dict
    :param strip_ns: Flag for whether to remove the namespaces from the tags.
    :type strip_ns: bool
    """
    paths = paths or ['.//']
    nsmap = nsmap or {}
    fields = defaultdict(list)
    for path in paths:
        elements = tree.findall(path, nsmap)
        for element in elements:
            tag = re.sub(
                r'\{.*\}', '', element.tag) if strip_ns else element.tag
            fields[tag].append(element.text)
    return dict(fields)
