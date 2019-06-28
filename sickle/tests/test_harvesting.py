# coding: utf-8
"""
    sickle.tests.test_harvesting
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2015 Mathias Loesch
"""
import os
import unittest

from lxml import etree
from nose.tools import raises
import mock

from sickle import Sickle
from sickle._compat import binary_type, string_types, text_type, to_unicode
from sickle.response import OAIResponse
from sickle.iterator import OAIResponseIterator
from sickle.oaiexceptions import BadArgument, CannotDisseminateFormat, \
    IdDoesNotExist, NoSetHierarchy, BadResumptionToken, NoRecordsMatch, \
    OAIError

this_dir, this_filename = os.path.split(__file__)


class MockResponse(object):
    """Mimics the response object returned by HTTP requests."""

    def __init__(self, text):
        # request's response object carry an attribute 'text' which contains
        # the server's response data encoded as unicode.
        self.text = text
        self.content = text.encode('utf-8')


def mock_harvest(*args, **kwargs):
    """Read test data from files instead of from an OAI interface.

    The data is read from the ``xml`` directory by using the provided
    :attr:`verb` as file name. The following returns an OAIResponse created
    from the file ``ListRecords.xml``::

        fake_harvest(verb='ListRecords', metadataPrefix='oai_dc')

    The file names for consecutive resumption responses are expected in the
    resumptionToken parameter::

        fake_harvest(verb='ListRecords', resumptionToken='ListRecords2.xml')

    The parameter :attr:`error` can be used to invoke a specific OAI error
    response. For instance, the following returns a ``badArgument`` error
    response::

        fake_harvest(verb='ListRecords', error='badArgument')

    :param kwargs: OAI arguments that would normally be passed to
                   :meth:`sickle.app.Sickle.harvest`.
    :rtype: :class:`sickle.response.OAIResponse`.
    """
    verb = kwargs.get('verb')
    resumption_token = kwargs.get('resumptionToken')
    error = kwargs.get('error')
    if resumption_token is not None:
        filename = resumption_token
    elif error is not None:
        filename = '%s.xml' % error
    else:
        filename = '%s.xml' % verb

    with open(os.path.join(this_dir, 'sample_data', filename), 'r') as fp:
        response = MockResponse(to_unicode(fp.read()))
        return OAIResponse(response, kwargs)


class TestCase(unittest.TestCase):


    def __init__(self, methodName='runTest'):
        super(TestCase, self).__init__(methodName)
        self.patch = mock.patch('sickle.app.Sickle.harvest', mock_harvest)

    def setUp(self):
        self.patch.start()
        self.sickle = Sickle('http://localhost')

    def tearDown(self):
        self.patch.stop()

    def test_OAIResponse(self):
        response = self.sickle.harvest(verb='ListRecords',
                                       metadataPrefix='oai_dc')
        self.assertIsInstance(response.xml, etree._Element)
        self.assertIsInstance(response.raw, string_types)

    def test_broken_XML(self):
        response = self.sickle.harvest(
            verb='ListRecords', resumptionToken='ListRecordsBroken.xml')
        self.assertEqual(response.xml, None)
        self.assertIsInstance(response.raw, string_types)

    def test_ListRecords(self):
        records = self.sickle.ListRecords(metadataPrefix='oai_dc')
        assert len([r for r in records]) == 8

    def test_ListRecords_ignore_deleted(self):
        records = self.sickle.ListRecords(metadataPrefix='oai_dc',
                                          ignore_deleted=True)
        num_records = len([r for r in records])
        assert num_records == 4

    def test_ListSets(self):
        set_iterator = self.sickle.ListSets()
        sets = [s for s in set_iterator]
        self.assertEqual(131, len(sets))
        dict(sets[0])

    def test_ListMetadataFormats(self):
        mdf_iterator = self.sickle.ListMetadataFormats()
        mdfs = [mdf for mdf in mdf_iterator]
        self.assertEqual(5, len(mdfs))
        dict(mdfs[0])

    def test_ListIdentifiers(self):
        records = self.sickle.ListIdentifiers(metadataPrefix='oai_dc')
        self.assertEqual(len([r for r in records]), 4)

    def test_ListIdentifiers_ignore_deleted(self):
        records = self.sickle.ListIdentifiers(
            metadataPrefix='oai_dc', ignore_deleted=True)
        # There are 2 deleted headers in the test data
        num_records = len([r for r in records])
        self.assertEqual(num_records, 2)

    def test_Identify(self):
        identify = self.sickle.Identify()
        self.assertTrue(hasattr(identify, 'repositoryName'))
        self.assertTrue(hasattr(identify, 'baseURL'))
        self.assertTrue(hasattr(identify, 'adminEmail'))
        self.assertTrue(hasattr(identify, 'earliestDatestamp'))
        self.assertTrue(hasattr(identify, 'deletedRecord'))
        self.assertTrue(hasattr(identify, 'granularity'))
        self.assertTrue(hasattr(identify, 'description'))
        self.assertTrue(hasattr(identify, 'oai_identifier'))
        self.assertTrue(hasattr(identify, 'sampleIdentifier'))
        dict(identify)

    def test_GetRecord(self):
        oai_id = 'oai:test.example.com:1996652'
        record = self.sickle.GetRecord(identifier=oai_id)
        self.assertEqual(record.header.identifier, oai_id)
        self.assertIn(oai_id, record.raw)
        self.assertEqual(record.header.datestamp, '2011-09-05T12:51:52Z')
        self.assertIsInstance(record.xml, etree._Element)
        binary_type(record)
        text_type(record)
        dict(record.header)
        self.assertEqual(dict(record), record.metadata)

    # Test OAI-specific exceptions

    @raises(BadArgument)
    def test_badArgument(self):
        self.sickle.ListRecords(metadataPrefix='oai_dc',
                                error='badArgument')

    @raises(CannotDisseminateFormat)
    def test_cannotDisseminateFormat(self):
        self.sickle.ListRecords(
            metadataPrefix='oai_dc', error='cannotDisseminateFormat')

    @raises(IdDoesNotExist)
    def test_idDoesNotExist(self):
        self.sickle.GetRecord(
            metadataPrefix='oai_dc', error='idDoesNotExist')

    @raises(NoSetHierarchy)
    def test_noSetHierarchy(self):
        self.sickle.ListSets(
            metadataPrefix='oai_dc', error='noSetHierarchy')

    @raises(BadResumptionToken)
    def test_badResumptionToken(self):
        self.sickle.ListRecords(
            metadataPrefix='oai_dc', error='badResumptionToken')

    @raises(NoRecordsMatch)
    def test_noRecordsMatch(self):
        self.sickle.ListRecords(
            metadataPrefix='oai_dc', error='noRecordsMatch')

    @raises(OAIError)
    def test_undefined_OAI_error_XML(self):
        self.sickle.ListRecords(
            metadataPrefix='oai_dc', error='undefinedError')

    def test_OAIResponseIterator(self):
        sickle = Sickle('fake_url', iterator=OAIResponseIterator)
        records = [r for r in sickle.ListRecords(metadataPrefix='oai_dc')]
        self.assertEqual(len(records), 4)


def mock_get(*args, **kwargs):
    class MockResponseWrongEncoding(object):
        """Mimics a case where the requests library misidentifies the text encoding.

        If http headers do not specify the correct encoding, requests will default
        to 'ISO-8859-1', even though the oai-pmh document might specify e.g.
        <xml encoding='utf-8'>.

        Parameters
        ----------
        filename : str
            Name of a utf8-encoded test file in the sample_data directory.

        Attributes
        ----------
        content : bytes (py3) / str (py2)
            Raw utf8-encoded bytestream
        text : str (py3) / unicode (py2)
            Unicode string from self.content, but wrongly decoded as ISO-8859-1
        status_code : int
            = 200
        """

        def __init__(self, filename='GetRecord_utf8test.xml'):
            with open(os.path.join(this_dir, 'sample_data', filename), 'rb') as fp:
                self.content = fp.read()
            self.text = self.content.decode('ISO-8859-1')
            self.status_code = 200

        def raise_for_status(self):
            pass

    return MockResponseWrongEncoding()


class TestCaseWrongEncoding(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(TestCaseWrongEncoding, self).__init__(methodName)
        self.patch = mock.patch('sickle.app.requests.get', mock_get)

    def setUp(self):
        self.patch.start()
        self.sickle = Sickle('http://localhost')

    def tearDown(self):
        self.patch.stop()

    def test_GetRecord(self):
        oai_id = 'oai:test.example.com:1996652'
        record = self.sickle.GetRecord(identifier=oai_id)
        self.assertEqual(record.header.identifier, oai_id)
        self.assertIn(oai_id, record.raw)
        self.assertEqual(record.header.datestamp, '2011-09-05T12:51:52Z')
        self.assertIsInstance(record.xml, etree._Element)
        binary_type(record)
        text_type(record)
        dict(record.header)
        self.assertEqual(dict(record), record.metadata)
        self.assertIn(u'某人', record.metadata['creator'])
