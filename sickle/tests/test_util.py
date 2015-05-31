# coding: utf-8
"""
    sickle.tests.test_util
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2015 Mathias Loesch
"""
from unittest import TestCase

from lxml import etree

from sickle.utils import xml_to_dict


class TestUtils(TestCase):
    def test_xml_to_dict(self):
        xml = """\
<root>
    <a>One</a>
    <b>Two</b>
    <c>Three</c>
    <c>Four</c>
    <d/>
</root>"""

        self.assertEqual(xml_to_dict(etree.XML(xml)),
                         dict(a=['One'], b=['Two'], c=['Three', 'Four'],
                              d=[None]))
