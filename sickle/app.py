# coding: utf-8
"""
    Sickle
    ~~~~~~

    An OAI-PMH client.

    :copyright: Copright 2013 Mathias Loesch
"""

import time
import requests
from lxml import etree

from .models import Set, Record, Header, MetadataFormat, Identify
import oaiexceptions

import logging

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

OAI_NAMESPACE = '{http://www.openarchives.org/OAI/%s/}'
XMLParser = etree.XMLParser(remove_blank_text=True, recover=True)


# Map OAI verbs to class representations
DEFAULT_CLASS_MAPPING = {
    'GetRecord': Record,
    'ListRecords': Record,
    'ListIdentifiers': Header,
    'ListSets': Set,
    'ListMetadataFormats': MetadataFormat,
    'Identify': Identify,
}

# Map OAI verbs to the XML elements
VERBS_ELEMENTS = {
    'GetRecord': 'record',
    'ListRecords': 'record',
    'ListIdentifiers': 'header',
    'ListSets': 'set',
    'ListMetadataFormats': 'metadataFormat',
    'Identify': 'Identify',
}


class Sickle(object):
    """Client for harvesting OAI interfaces.

    Use it like this::

        >>> sickle = Sickle('http://elis.da.ulcc.ac.uk/cgi/oai2')
        >>> records = sickle.ListRecords(metadataPrefix='oai_dc')
        >>> records.next()
        <Record oai:eprints.rclis.org:3780>

    :param endpoint: The endpoint of the OAI interface.
    :type endpoint: str
    :param http_method: Method used for requests (GET or POST, default: GET).
    :type http_method: str
    :param protocol_version: The OAI protocol version.
    :type protocol_version: str
    :param max_retries: Number of retries if HTTP request fails.
    :type max_retries: int
    :param timeout: Timeout for HTTP requests.
    :type timeout: int
    :type protocol_version: str
    :param class_mapping: A dictionary that maps OAI verbs to classes representing
                          OAI items. If not provided,
                          :data:`sickle.app.DEFAULT_CLASS_MAPPING` will be used.
    :type class_mapping: dict
    :param auth: An optional tuple ('username', 'password')
                 for accessing protected OAI interfaces.
    :type auth: tuple
    """
    def __init__(self, endpoint, http_method='GET', protocol_version='2.0',
                 max_retries=5, timeout=None, class_mapping=None, auth=None):
        self.endpoint = endpoint
        if http_method not in ['GET', 'POST']:
            raise ValueError("Invalid HTTP method: %s! Must be GET or POST.")
        if protocol_version not in ['2.0', '1.0']:
            raise ValueError(
                "Invalid protocol version: %s! Must be 1.0 or 2.0.")
        self.http_method = http_method
        self.protocol_version = protocol_version
        self.max_retries = max_retries
        self.timeout = timeout
        self.oai_namespace = OAI_NAMESPACE % self.protocol_version
        if class_mapping is None:
            self.class_mapping = DEFAULT_CLASS_MAPPING
        else:
            self.class_mapping = class_mapping
        self.auth = auth
        self.last_response = None

    def harvest(self, **kwargs):
        """Make HTTP requests to the OAI server.

        :param kwargs: The OAI HTTP arguments.
        :rtype: :class:`sickle.app.OAIResponse`
        """
        for _ in xrange(self.max_retries):
            if self.http_method == 'GET':
                http_response = requests.get(self.endpoint, params=kwargs,
                                             timeout=self.timeout, auth=self.auth)
            else:
                http_response = requests.post(self.endpoint, data=kwargs,
                                              timeout=self.timeout, auth=self.auth)
            if http_response.status_code == 503:
                try:
                    retry_after = int(http_response.headers.get('retry-after'))
                except TypeError:
                    retry_after = 20
                print "Waiting %d seconds ... " % retry_after
                time.sleep(retry_after)
            else:
                http_response.raise_for_status()
                return OAIResponse(http_response, params=kwargs)

    def ListRecords(self, ignore_deleted=False, **kwargs):
        """Issue a ListRecords request.

        :param ignore_deleted: If set to :obj:`True`, the resulting
                              :class:`sickle.app.OAIIterator` will skip records
                              flagged as deleted.
        :rtype: :class:`sickle.app.OAIIterator`
        """
        params = kwargs
        params.update({'verb': 'ListRecords'})
        self.last_response = self.harvest(**params)
        return OAIIterator(self.last_response, self, ignore_deleted=ignore_deleted)

    def ListIdentifiers(self, ignore_deleted=False, **kwargs):
        """Issue a ListIdentifiers request.

        :param ignore_deleted: If set to :obj:`True`, the resulting
                              :class:`sickle.app.OAIIterator` will skip records
                              flagged as deleted.
        :rtype: :class:`sickle.app.OAIIterator`
        """
        params = kwargs
        params.update({'verb': 'ListIdentifiers'})
        self.last_response = self.harvest(**params)
        return OAIIterator(self.last_response, self, ignore_deleted=ignore_deleted)

    def ListSets(self, **kwargs):
        """Issue a ListSets request.

        :rtype: :class:`sickle.app.OAIIterator`
        """
        params = kwargs
        params.update({'verb': 'ListSets'})
        self.last_response = self.harvest(**params)
        return OAIIterator(self.last_response, self)

    def Identify(self):
        """Issue an Identify request.

        :rtype: :class:`sickle.models.Identify`
        """
        params = {'verb': 'Identify'}
        self.last_response = self.harvest(**params)
        return Identify(self.last_response)

    def GetRecord(self, **kwargs):
        """Issue a ListSets request.

        :rtype: :class:`sickle.models.Record`
        """
        params = kwargs
        params.update({'verb': 'GetRecord'})
        self.last_response = self.harvest(**params)
        # GetRecord is treated as a special case of ListRecords:
        # by creating an OAIIterator and returning the first and
        # only record.
        return OAIIterator(self.last_response, self).next()

    def ListMetadataFormats(self, **kwargs):
        """Issue a ListMetadataFormats request.

        :rtype: :class:`sickle.app.OAIIterator`
        """
        params = kwargs
        params.update({'verb': 'ListMetadataFormats'})
        self.last_response = self.harvest(**params)
        return OAIIterator(self.last_response, self)


class OAIResponse(object):
    """A response from an OAI server.

    Provides access to the returned data on different abstraction
    levels.

    :param response: The original HTTP response.
    :param params: The OAI parameters for the request.
    :type params: dict
    """
    def __init__(self, http_response, params):
        self.params = params
        self.http_response = http_response

    @property
    def raw(self):
        """The server's response as unicode."""
        return self.http_response.text

    @property
    def xml(self):
        """The server's response as parsed XML."""
        return etree.XML(self.http_response.text.encode("utf8"), parser=XMLParser)

    def __repr__(self):
        return '<OAIResponse %s>' % self.params.get('verb')


class OAIIterator(object):
    """Iterator over OAI records/identifiers/sets transparently aggregated via
    OAI-PMH.

    Can be used to conveniently iterate through the records of a repository.

    :param oai_response: The first OAI response.
    :type oai_response: :class:`sickle.app.OAIResponse`
    :param sickle: The Sickle object that issued the first request.
    :type sickle: :class:`sickle.app.Sickle`
    :param ignore_deleted: Flag for whether to ignore deleted records.
    :type ignore_deleted: bool
    """
    def __init__(self, oai_response, sickle, ignore_deleted=False):
        self.oai_response = oai_response
        self.sickle = sickle
        self.verb = self.oai_response.params.get("verb")
        # Determine on what element to iterate (records, headers, or sets)
        self.element = VERBS_ELEMENTS[self.verb]
        # Get the reflection class for the elements returned by this verb
        self.mapper = self.sickle.class_mapping[self.verb]
        error = self.oai_response.xml.find(
            './/' + self.sickle.oai_namespace + 'error')
        if error is not None:
            code = error.attrib.get('code', 'UNKNOWN')
            description = error.text or ''
            try:
                raise getattr(
                    oaiexceptions, code[0].upper() + code[1:])(description)
            except AttributeError:
                raise oaiexceptions.OAIError(description)

        self._items = self.oai_response.xml.iterfind(
            './/' + self.sickle.oai_namespace + self.element)
        self.resumption_token = self._get_resumption_token()
        self.ignore_deleted = ignore_deleted

    def __iter__(self):
        return self

    def __repr__(self):
        return '<OAIIterator %s>' % self.verb

    def _get_resumption_token(self):
        """Extract and store the resumptionToken from the last response."""
        resumption_token = self.oai_response.xml.find(
            './/' + self.sickle.oai_namespace + 'resumptionToken')
        if resumption_token is None:
            return None
        else:
            return resumption_token.text

    def _next_response(self):
        """Get the next response from the OAI server."""
        self.oai_response = self.sickle.harvest(verb=self.verb,
                                                resumptionToken=self.resumption_token)
        logger.debug('Getting next response (resumptionToken: %s' %
                     self.resumption_token)
        self.resumption_token = self._get_resumption_token()
        self._items = self.oai_response.xml.iterfind(
            './/' + self.sickle.oai_namespace + self.element)

    def next(self):
        """Return the next record/header/set."""
        try:
            while True:
                mapped = self.mapper(self._items.next())
                if self.ignore_deleted:
                    if mapped.deleted:
                        continue
                return mapped
        except StopIteration:
            if self.resumption_token is None:
                raise StopIteration
            else:
                self._next_response()
                while True:
                    mapped = self.mapper(self._items.next())
                    if self.ignore_deleted and mapped.deleted:
                        continue
                    return mapped
