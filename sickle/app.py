# coding: utf-8
"""
    Sickle
    ~~~~~~

    An OAI-PMH client.

    :copyright: Copright 2013 Mathias Loesch
"""


from .models import Set, Record, Header, MetadataFormat, Identify
import oaiexceptions

import requests
from lxml import etree

OAI_NAMESPACE = '{http://www.openarchives.org/OAI/%s/}'
XMLParser = etree.XMLParser(remove_blank_text=True)


class Sickle(object):
    """Client for harvesting OAI interfaces.

    Use it like this::

        >>> sickle = Sickle('http://elis.da.ulcc.ac.uk/cgi/oai2')
        >>> response = sickle.ListRecords(metadataPrefix='oai_dc')


    :param endpoint: The endpoint of the OAI interface.
    :type endpoint: str
    :param http_method: Method used for requests (GET or POST).
    :type http_method: str
    :param protocol_version: The OAI protocol version.
    :type protocol_version: str
    """
    def __init__(self, endpoint, http_method='GET', protocol_version='2.0'):
        super(Sickle, self).__init__()
        self.endpoint = endpoint
        self.http_method = http_method
        self.protocol_version = protocol_version
        self.oai_namespace = OAI_NAMESPACE % self.protocol_version
        self.last_response = None

    def harvest(self, **kwargs):
        """Make an HTTP request to the OAI server."""
        if self.http_method == 'GET':
            return OAIResponse(requests.get(self.endpoint, params=kwargs), 
                params=kwargs)
        elif self.http_method == 'POST':
            return OAIResponse(requests.post(self.endpoint, data=kwargs), 
                params=kwargs)

    def ListRecords(self, ignore_deleted=False, **kwargs):
        """Issue a ListRecords request.e

        :rtype: :class:`~sickle.app.OAIResponse`
        """
        params = kwargs
        params.update({'verb': 'ListRecords'})
        self.last_response = self.harvest(**params)
        return OAIIterator(self.last_response, self, ignore_deleted=ignore_deleted)

    def ListIdentifiers(self, ignore_deleted=False, **kwargs):
        """Issue a ListIdentifiers request.

        :rtype: :class:`~sickle.app.OAIResponse`
        """
        params = kwargs
        params.update({'verb': 'ListIdentifiers'})
        self.last_response = self.harvest(**params)
        return OAIIterator(self.last_response, self, ignore_deleted=ignore_deleted)

    def ListSets(self, **kwargs):
        """Issue a ListSets request.

        :rtype: :class:`~sickle.app.OAIResponse`
        """
        params = kwargs
        params.update({'verb': 'ListSets'})
        self.last_response = self.harvest(**params)
        return OAIIterator(self.last_response, self)

    def Identify(self):
        """Issue an Identify request.

        :rtype: :class:`~sickle.app.OAIResponse`
        """
        params = {'verb': 'Identify'}
        self.last_response = self.harvest(**params)
        return Identify(self.last_response)

    def GetRecord(self, **kwargs):
        """Issue a ListSets request.

        :rtype: :class:`~sickle.app.OAIResponse`
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

        :rtype: :class:`~sickle.app.OAIResponse`
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
    def __init__(self, response, params):
        self.params = params
        self.response = response

    @property
    def raw(self):
        """The server's response as unicode."""
        return self.response.text

    @property
    def xml(self):
        """The server's response as parsed XML."""
        return etree.XML(self.response.text.encode("utf8"), parser=XMLParser)

    def __repr__(self):
        return '<OAIResponse %s>' % self.params.get('verb')


class OAIIterator(object):
    """Iterator over OAI records/identifiers/sets transparently aggregated via
    OAI-PMH.

    Can be used to conveniently iterate through the records of a repository::

        >>> oai_response = sickle.ListRecords(metadataPrefix='oai_dc')
        >>> records = oai_response.iter()
        >>> records.next()
        <Element {http://www.openarchives.org/OAI/2.0/}record at 0x1051b3b90>

    :param oai_response: The first OAI response.
    :type oai_response: :class:`~sickle.app.OAIResponse`
    :param sickle: The Sickle object that issued the first request.
    :type sickle: :class:`~sickle.app.Sickle`
    :param ignore_deleted: Flag for whether to ignore deleted records.
    :type ignore_deleted: bool
    """
    def __init__(self, oai_response, sickle, ignore_deleted=False):
        self.oai_response = oai_response
        self.sickle = sickle
        self.verb = self.oai_response.params.get("verb")
        # Determine on what element to iterate (records, headers, or sets)
        if self.verb == 'ListRecords' or self.verb == 'GetRecord':
            self.element = 'record'
            self.mapper = Record
        elif self.verb == 'ListIdentifiers':
            self.element = 'header'
            self.mapper = Header
        elif self.verb == 'ListSets':
            self.element = 'set'
            self.mapper = Set
        elif self.verb == 'ListMetadataFormats':
            self.element = 'metadataFormat'
            self.mapper = MetadataFormat
        error = self.oai_response.xml.find('.//' + self.sickle.oai_namespace + 'error')
        if error is not None:
            code = error.attrib.get('code', 'UNKNOWN')
            description = error.text or ''
            try:
                raise getattr(oaiexceptions, code[0].upper() + code[1:]), description
            except AttributeError:
                raise oaiexceptions.OAIError, description

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
        self.resumption_token = self._get_resumption_token()
        self._items = self.oai_response.xml.iterfind(
            './/' + self.sickle.oai_namespace + self.element)

    def next(self):
        """Return the next record/header/set."""
        try:
            while True:
                mapped = self.mapper(self._items.next())
                if self.ignore_deleted and mapped.deleted:
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
