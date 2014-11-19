# coding: utf-8
"""
    sickle.utils
    ~~~~~~~~~~~~

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

def xml_to_nested_dict(tree, strip_ns=False):
    """Convert an XML tree into a nested dictionary. This is an alternative to
    xml_to_dict but allows the structure to be maintained.

    :param strip_ns: Flag for whether to remove the namespaces from the tags.
    """
    fields = {}
    for n in tree.findall('./'):
        # strip out namespace if required
        tag = re.sub(r'\{.*\}', '', n.tag) if strip_ns else n.tag

        # fetch correct content, recursive if nested elements, text if not.
        content = n.text if n.text is not None else xml_to_nested_dict(
            n, strip_ns=strip_ns)

        # if there are multiple elements with the same tag, coernce them into
        # a list
        if tag in fields:
            if isinstance(fields[tag], list):
                fields[tag].append(content)
            else:
                fields[tag] = [fields[tag], content]
        else:
            fields[tag] = content

    return fields
