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
        with patch('sickle.app.requests.get', mock_get):
            sickle = Sickle('url', timeout=10, proxies=dict(),
                            auth=('user', 'password'))
            sickle.ListRecords()
            mock_get.assert_called_once_with('url',
                                             params={'verb': 'ListRecords'},
                                             timeout=10, proxies=dict(),
                                             auth=('user', 'password'))

    def test_override_encoding(self):
        mock_response = Mock(text='<xml/>', content='<xml/>', status_code=200)
        mock_get = Mock(return_value=mock_response)
        with patch('sickle.app.requests.get', mock_get):
            sickle = Sickle('url', encoding='encoding')
            sickle.ListSets()
            mock_get.assert_called_once_with('url',
                                             params={'verb': 'ListSets'})

    def test_no_retry(self):
        mock_response = Mock(status_code=503,
                             headers={'retry-after': '10'},
                             raise_for_status=Mock(side_effect=HTTPError))
        mock_get = Mock(return_value=mock_response)
        with patch('sickle.app.requests.get', mock_get):
            sickle = Sickle('url')
            try:
                sickle.ListRecords()
            except HTTPError:
                pass
            self.assertEqual(1, mock_get.call_count)

    def test_retry_on_503(self):
        mock_response = Mock(status_code=503,
                             headers={'retry-after': '10'},
                             raise_for_status=Mock(side_effect=HTTPError))
        mock_get = Mock(return_value=mock_response)
        sleep_mock = Mock()
        with patch('time.sleep', sleep_mock):
            with patch('sickle.app.requests.get', mock_get):
                sickle = Sickle('url', max_retries=3, default_retry_after=0)
                try:
                    sickle.ListRecords()
                except HTTPError:
                    pass
                mock_get.assert_called_with('url',
                                            params={'verb': 'ListRecords'})
                self.assertEqual(4, mock_get.call_count)
                self.assertEqual(3, sleep_mock.call_count)
                sleep_mock.assert_called_with(10)

    def test_retry_on_custom_code(self):
        mock_response = Mock(status_code=500,
                             raise_for_status=Mock(side_effect=HTTPError))
        mock_get = Mock(return_value=mock_response)
        with patch('sickle.app.requests.get', mock_get):
            sickle = Sickle('url', max_retries=3, default_retry_after=0, retry_status_codes=(503, 500))
            try:
                sickle.ListRecords()
            except HTTPError:
                pass
            mock_get.assert_called_with('url',
                                        params={'verb': 'ListRecords'})
            self.assertEqual(4, mock_get.call_count)
