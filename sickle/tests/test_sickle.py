# coding: utf-8
"""
    sickle.tests.test_sickle
    ~~~~~~~~~~~~~~~~~~~~~~~~
"""
import os

from sickle import Sickle
from nose.tools import assert_raises, assert_true, raises


this_dir, this_filename = os.path.split(__file__)

@raises(ValueError)
def test_wrong_http_meth():
    sickle = Sickle("http://localhost", http_method="GHOST")


@raises(ValueError)
def test_wrong_protocol_version():
    sickle = Sickle("http://localhost", protocol_version="3.0")


@raises(ValueError)
def test_wrong_protocol_version():
    sickle = Sickle("http://localhost", protocol_version="3.0")
