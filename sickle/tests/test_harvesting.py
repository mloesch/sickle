# coding: utf-8
"""
    sickle.tests.test_harvesting
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import os

from sickle import Sickle, OAIResponse
from sickle.oaiexceptions import BadArgument, CannotDisseminateFormat,\
    IdDoesNotExist, NoSetHierarchy, BadResumptionToken, NoRecordsMatch, OAIError
from nose.tools import assert_raises, assert_true, raises

import unittest
import mock

this_dir, this_filename = os.path.split(__file__)


class FakeResponse(object):

    """Mimics the response object returned by HTTP requests."""
    def __init__(self, text):
        # request's response object carry an attribute 'text' which contains
        # the server's response data encoded as unicode.
        self.text = text


def fake_harvest(*args, **kwargs):
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
    :rtype: :class:`sickle.app.OAIResponse`.
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
    response = FakeResponse(open(
        os.path.join(this_dir, 'sample_data', filename), 'r').read().decode('utf8'))

    return OAIResponse(response, kwargs)


class TestCase(unittest.TestCase):

    def setUp(self):
        mock.patch('sickle.app.Sickle.harvest', fake_harvest).start()
        self.sickle = Sickle('fake_url')

    def test_OAIResponse(self):
        response = self.sickle.harvest(verb='ListRecords', metadataPrefix='oai_dc')
        response.xml
        response.raw

    def test_broken_XML(self):
        response = self.sickle.harvest(
            verb='ListRecords', resumptionToken='ListRecordsBroken.xml')
        response.xml
        response.raw

    def test_ListRecords(self):
        records = self.sickle.ListRecords(metadataPrefix='oai_dc')
        assert len([r for r in records]) == 8

    def test_ListRecords_ignore_deleted(self):
        records = self.sickle.ListRecords(metadataPrefix='oai_dc', ignore_deleted=True)
        # There are twelve deleted records in the test data
        num_records = len([r for r in records])
        assert num_records == 4


    def test_ListSets(self):

        sets = self.sickle.ListSets()
        num_sets = len([s for s in sets])
        assert num_sets == 131
        dict(s)

    def test_ListMetadataFormats(self):
        mdfs = self.sickle.ListMetadataFormats()
        num_mdfs = len([mdf for mdf in mdfs])
        assert num_mdfs == 5

        dict(mdf)

    def test_ListIdentifiers(self):
        records = self.sickle.ListIdentifiers(metadataPrefix='oai_dc')
        assert len([r for r in records]) == 4

    def test_ListIdentifiers_ignore_deleted(self):
        records = self.sickle.ListIdentifiers(
            metadataPrefix='oai_dc', ignore_deleted=True)
            # There are 2 deleted headers in the test data
        num_records = len([r for r in records])
        assert num_records == 2


    def test_Identify(self):
        identify = self.sickle.Identify()
        assert hasattr(identify, 'repositoryName')
        assert hasattr(identify, 'baseURL')
        assert hasattr(identify, 'adminEmail')
        assert hasattr(identify, 'earliestDatestamp')
        assert hasattr(identify, 'deletedRecord')
        assert hasattr(identify, 'granularity')
        assert hasattr(identify, 'description')
        assert hasattr(identify, 'oai_identifier')
        assert hasattr(identify, 'sampleIdentifier')
        dict(identify)

    def test_GetRecord(self):
        oai_id = 'oai:test.example.com:1996652'
        record = self.sickle.GetRecord(identifier=oai_id)
        assert record.header.identifier == oai_id
        assert oai_id in record.raw
        record.xml
        str(record)
        unicode(record)
        dict(record.header)
        dict(record.about)
        assert dict(record) == record.metadata

    # Test OAI-specific exceptions

    @raises(BadArgument)
    def test_badArgument(self):
        records = self.sickle.ListRecords(metadataPrefix='oai_dc',
            error='badArgument')

    @raises(CannotDisseminateFormat)
    def test_cannotDisseminateFormat(self):
        records = self.sickle.ListRecords(
            metadataPrefix='oai_dc', error='cannotDisseminateFormat')

    @raises(IdDoesNotExist)
    def test_idDoesNotExist(self):
        records = self.sickle.GetRecord(
            metadataPrefix='oai_dc', error='idDoesNotExist')

    @raises(NoSetHierarchy)
    def test_idDoesNotExist(self):
        records = self.sickle.ListSets(
            metadataPrefix='oai_dc', error='noSetHierarchy')


    @raises(BadResumptionToken)
    def test_badResumptionToken(self):
        records = self.sickle.ListRecords(
            metadataPrefix='oai_dc', error='badResumptionToken')

    @raises(NoRecordsMatch)
    def test_noRecordsMatch(self):
        records = self.sickle.ListRecords(
            metadataPrefix='oai_dc', error='noRecordsMatch')

    @raises(OAIError)
    def test_undefined_OAI_error_XML(self):
        records = self.sickle.ListRecords(
            metadataPrefix='oai_dc', error='undefinedError')

    @mock.patch('sickle.app.Sickle.harvest', fake_harvest)
    def test_OAIResponseIterator(self):
        sickle = Sickle('fake_url', rtype='response')
        records = [r for r in sickle.ListRecords(metadataPrefix='oai_dc')]
        assert len(records) == 4
