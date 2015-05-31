# coding: utf-8
"""
    sickle.tests.test_sickle
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2015 Mathias Loesch
"""
import os
import unittest

from nose.tools import raises

from sickle import Sickle

this_dir, this_filename = os.path.split(__file__)


class TestCase(unittest.TestCase):
    @raises(ValueError)
    def test_invalid_http_method(self):
        Sickle("http://localhost", http_method="DELETE")

    @raises(ValueError)
    def test_wrong_protocol_version(self):
        Sickle("http://localhost", protocol_version="3.0")

    @raises(TypeError)
    def test_invalid_iterator(self):
        Sickle("http://localhost", iterator=None)
