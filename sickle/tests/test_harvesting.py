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
        os.path.join(this_dir, 'xml', filename), 'r').read().decode('utf8'))

    return OAIResponse(response, kwargs)


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
def test_OAIResponse():
    sickle = Sickle('fake_url')
    response = sickle.harvest(verb='ListRecords', metadataPrefix='oai_dc')
    response.xml
    response.raw


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
def test_broken_XML():
    sickle = Sickle('fake_url')
    response = sickle.harvest(
        verb='ListRecords', resumptionToken='ListRecordsBroken.xml')
    response.xml
    response.raw


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
def test_ListRecords():
    sickle = Sickle('fake_url')
    records = sickle.ListRecords(metadataPrefix='oai_dc')
    assert len([r for r in records]) == 400


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
def test_ListRecords_ignore_deleted():
    sickle = Sickle('fake_url')
    records = sickle.ListRecords(metadataPrefix='oai_dc', ignore_deleted=True)
    # There are twelve deleted records in the test data
    num_records = len([r for r in records])
    assert num_records == 388


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
def test_ListSets():
    sickle = Sickle('fake_url')
    sets = sickle.ListSets()
    num_sets = len([s for s in sets])
    assert num_sets == 131
    dict(s)


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
def test_ListMetadataFormats():
    sickle = Sickle('fake_url')
    mdfs = sickle.ListMetadataFormats()
    num_mdfs = len([mdf for mdf in mdfs])
    assert num_mdfs == 5

    dict(mdf)


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
def test_ListIdentifiers():
    sickle = Sickle('fake_url')
    records = sickle.ListIdentifiers(metadataPrefix='oai_dc')
    assert len([r for r in records]) == 400


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
def test_ListIdentifiers_ignore_deleted():
    sickle = Sickle('fake_url')
    records = sickle.ListIdentifiers(
        metadataPrefix='oai_dc', ignore_deleted=True)
    # There are ten deleted headers in the test data
    num_records = len([r for r in records])
    assert num_records == 390


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
def test_Identify():
    sickle = Sickle('fake_url')
    identify = sickle.Identify()
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


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
def test_GetRecord():
    sickle = Sickle('fake_url')
    oai_id = 'oai:test.example.com:1996652'
    record = sickle.GetRecord(identifier=oai_id)
    assert record.header.identifier == oai_id
    assert oai_id in record.raw
    record.xml
    str(record)
    unicode(record)
    dict(record.header)
    assert dict(record) == record.metadata

# Test OAI-specific exceptions


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
@raises(BadArgument)
def test_badArgument():
    sickle = Sickle('fake_url')
    records = sickle.ListRecords(metadataPrefix='oai_dc', error='badArgument')


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
@raises(CannotDisseminateFormat)
def test_cannotDisseminateFormat():
    sickle = Sickle('fake_url')
    records = sickle.ListRecords(
        metadataPrefix='oai_dc', error='cannotDisseminateFormat')


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
@raises(IdDoesNotExist)
def test_idDoesNotExist():
    records = sickle.GetRecord(
        metadataPrefix='oai_dc', error='idDoesNotExist')


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
@raises(NoSetHierarchy)
def test_idDoesNotExist():
    sickle = Sickle('fake_url')
    records = sickle.ListSets(
        metadataPrefix='oai_dc', error='noSetHierarchy')


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
@raises(BadResumptionToken)
def test_badResumptionToken():
    sickle = Sickle('fake_url')
    records = sickle.ListRecords(
        metadataPrefix='oai_dc', error='badResumptionToken')


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
@raises(NoRecordsMatch)
def test_noRecordsMatch():
    sickle = Sickle('fake_url')
    records = sickle.ListRecords(
        metadataPrefix='oai_dc', error='noRecordsMatch')


@mock.patch('sickle.app.Sickle.harvest', fake_harvest)
@raises(OAIError)
def test_undefined_OAI_error_XML():
    sickle = Sickle('fake_url')
    records = sickle.ListRecords(
        metadataPrefix='oai_dc', error='undefinedError')
