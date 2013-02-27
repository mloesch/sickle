# coding: utf-8

import os

from sickle import Sickle, OAIResponse
from sickle.oaiexceptions import BadArgument, CannotDisseminateFormat,\
    IdDoesNotExist, NoSetHierarchy, BadResumptionToken, NoRecordsMatch
from nose.tools import assert_raises, assert_true, raises

import logging

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s",
                              "%d.%m.%Y %H:%M:%S")

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)


this_dir, this_filename = os.path.split(__file__)

# Create a Sickle OAI-PMH client. It doesn't need a resolvable
# OAI endpoint for testing since we are reading the responses 
# from files.
sickle = Sickle('fake_url')


class FakeResponse(object):
    """Mimics the response object returned by HTTP requests."""
    def __init__(self, text):
        # request's response object carry an attribute 'text' which contains
        # the server's response data encoded as unicode.
        self.text = text


def fake_harvest(**kwargs):
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

# Monkey patch the Sickle client object with the mock harvesting method
sickle.harvest = fake_harvest


def test_ListRecords():
    records = sickle.ListRecords(metadataPrefix='oai_dc')
    assert len([r for r in records]) == 400


def test_ListRecords_ignore_deleted():
    records = sickle.ListRecords(metadataPrefix='oai_dc', ignore_deleted=True)
    # There are twelve deleted records in the test data
    num_records = len([r for r in records])
    assert num_records == 388


def test_ListSets():
    sets = sickle.ListSets()
    num_sets = len([s for s in sets])
    assert num_sets == 131


def test_ListMetadataFormats():
    mdfs = sickle.ListMetadataFormats()
    num_mdfs = len([mdf for mdf in mdfs])
    assert num_mdfs == 5


def test_ListIdentifiers():
    records = sickle.ListIdentifiers(metadataPrefix='oai_dc')
    assert len([r for r in records]) == 400


def test_ListIdentifiers_ignore_deleted():
    records = sickle.ListIdentifiers(
        metadataPrefix='oai_dc', ignore_deleted=True)
    # There are ten deleted headers in the test data
    num_records = len([r for r in records])
    assert num_records == 390


def test_Identify():
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


def test_GetRecord():
    oai_id = 'oai:pub.ub.uni-bielefeld.de:1996652'
    record = sickle.GetRecord(identifier=oai_id)
    assert record.header.identifier == oai_id


@raises(BadArgument)
def test_badArgument():
    records = sickle.ListRecords(metadataPrefix='oai_dc', error='badArgument')


@raises(CannotDisseminateFormat)
def test_cannotDisseminateFormat():
    records = sickle.ListRecords(
        metadataPrefix='oai_dc', error='cannotDisseminateFormat')


@raises(IdDoesNotExist)
def test_idDoesNotExist():
    records = sickle.GetRecord(
        metadataPrefix='oai_dc', error='idDoesNotExist')


@raises(NoSetHierarchy)
def test_idDoesNotExist():
    records = sickle.ListSets(
        metadataPrefix='oai_dc', error='noSetHierarchy')


@raises(BadResumptionToken)
def test_badResumptionToken():
    records = sickle.ListRecords(
        metadataPrefix='oai_dc', error='badResumptionToken')


@raises(NoRecordsMatch)
def test_noRecordsMatch():
    records = sickle.ListRecords(
        metadataPrefix='oai_dc', error='noRecordsMatch')
