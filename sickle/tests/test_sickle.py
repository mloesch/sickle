# coding: utf-8
"""
    sickle.tests.test_sickle
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2015 Mathias Loesch
"""
import os
import unittest

from mock import patch, Mock
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

    def test_pass_request_args(self):
        mock_response = Mock(text='<xml/>')
        mock_get = Mock(return_value=mock_response)
        with patch('sickle.app.requests.get', mock_get):
            sickle = Sickle('url', timeout=10, proxies=dict(),
                            auth=('user', 'password'))
            sickle.ListRecords()
            mock_get.assert_called_once_with('url',
                                             params={'verb': 'ListRecords'},
                                             timeout=10, proxies=dict(),
                                             auth=('user', 'password'))

    def test_override_encoding(self):
        mock_response = Mock(text='<xml/>')
        mock_get = Mock(return_value=mock_response)
        with patch('sickle.app.requests.get', mock_get):
            sickle = Sickle('url', encoding='encoding')
            sickle.ListSets()
            self.assertEqual(mock_response.encoding, 'encoding')
