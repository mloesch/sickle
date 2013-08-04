# coding: utf-8
"""
    utils
    ~~~~~

    Collects utility functions.

    :copyright: Copright 2013 Mathias Loesch
"""

import re
from collections import defaultdict


def get_namespace(element):
    """Return the namespace of an XML element.

    :param element: An XML element.
    """
    return re.search('(\{.*\})', element.tag).group(1)


def xml_to_dict(tree, paths=['.//'], nsmap={}, strip_ns=False):
    """Convert an XML tree to a dictionary.

    :param paths: An optional list of XPath expressions applied on the XML tree.
    :param nsmap: An optional prefix-namespace mapping for conciser spec of paths.
    :param strip_ns: Flag for whether to remove the namespaces from the tags.
    """
    fields = defaultdict(list)
    for path in paths:
        elements = tree.findall(path, nsmap)
        for element in elements:
            tag = re.sub(
                r'\{.*\}', '', element.tag) if strip_ns else element.tag
            fields[tag].append(element.text)
    return dict(fields)
