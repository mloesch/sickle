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
from requests import HTTPError

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
        mock_response = Mock(text=u'<xml/>', content='<xml/>', status_code=200)
        mock_get = Mock(return_value=mock_response)
        sickle = Sickle('url', timeout=10, proxies=dict(),
                        auth=('user', 'password'))
        sickle.session.get = mock_get
        sickle.ListRecords()
        mock_get.assert_called_once_with('url',
                                         params={'verb': 'ListRecords'},
                                         timeout=10, proxies=dict(),
                                         auth=('user', 'password'))

    def test_override_encoding(self):
        mock_response = Mock(text='<xml/>', content='<xml/>', status_code=200)
        mock_get = Mock(return_value=mock_response)
        sickle = Sickle('url', encoding='encoding')
        sickle.session.get = mock_get
        sickle.ListSets()
        mock_get.assert_called_once_with('url',
                                         params={'verb': 'ListSets'})

    def test_no_retry(self):
        mock_response = Mock(status_code=503,
                             headers={'retry-after': '10'},
                             raise_for_status=Mock(side_effect=HTTPError))
        mock_get = Mock(return_value=mock_response)
        sickle = Sickle('url')
        sickle.session.get = mock_get
        try:
            sickle.ListRecords()
        except HTTPError:
            pass
        self.assertEqual(1, mock_get.call_count)

    def test_retry_arguments(self):
        sickle = Sickle('url', retry_backoff_factor=1.1234, max_retries=99, retry_status_codes=(418,))

        adapter = sickle.session.get_adapter('https://localhost/oai')
        retries = adapter.max_retries

        assert retries.total == 99
        assert retries.backoff_factor == 1.1234
        assert retries.status_forcelist == (418,)
        assert retries.method_whitelist == frozenset(['POST', 'GET'])
