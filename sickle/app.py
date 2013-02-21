# coding: utf-8
"""
    Sickle
    ~~~~~~

    An OAI-PMH client.

    :copyright: Copright 2013 Mathias Loesch
"""


import re
from collections import defaultdict
import requests
try:
    from lxml import etree
except ImportError:
    from xml.etree import ElementTree as etree


OAI_NAMESPACE = '{http://www.openarchives.org/OAI/%s/}'



def get_namespace(element):
    """Return the namespace of an XML element.

    :param element: An XML element.
    """
    return re.search('(\{.*\})', element.tag).group(1)


def xml_to_dict(tree, paths=['.//'], nsmap={}, strip_ns=False):
    """Convert an XML tree to a dictionary.

    :param paths: An optional list of XPath expressions applied on the XML tree.
    :param nsmap: An optional prefix-namespace mapping for conciser spec of paths.
    :param strip_ns: Flag for whether to remove the namespaces from the tags.
    """
    df = defaultdict(list)
    for path in paths:
        elements = tree.findall(path, nsmap)
        for element in elements:
            tag = element.tag
            if strip_ns:
                tag = re.sub(r'\{.*\}', '', tag)
            df[tag].append(element.text)
    return dict(df)



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

    def harvest(self, **kwargs):
        """Make an HTTP request to the OAI server."""
        if self.http_method == 'GET':
            return requests.get(self.endpoint, params=kwargs)
        elif self.http_method == 'POST':
            return requests.post(self.endpoint, data=kwargs)

    def ListRecords(self, **kwargs):
        """Issue a ListRecords request.

        :rtype: :class:`~sickle.app.OAIResponse`
        """
        params = kwargs
        params.update({'verb': 'ListRecords'})
        response = self.harvest(**params)
        return OAIResponse(response, params, self)

    def ListIdentifiers(self, **kwargs):
        """Issue a ListIdentifiers request.

        :rtype: :class:`~sickle.app.OAIResponse`
        """
        params = kwargs
        params.update({'verb': 'ListIdentifiers'})
        response = self.harvest(**params)
        return OAIResponse(response, params, self)

    def ListSets(self, **kwargs):
        """Issue a ListSets request.

        :rtype: :class:`~sickle.app.OAIResponse`
        """
        params = kwargs
        params.update({'verb': 'ListSets'})
        response = self.harvest(**params)
        return OAIResponse(response, params, self)

    def Identify(self):
        """Issue a ListSets request.

        :rtype: :class:`~sickle.app.OAIResponse`
        """
        params = {'verb': 'Identify'}
        response = self.harvest(**params)
        return OAIResponse(response, params, self)

    def GetRecord(self, **kwargs):
        """Issue a ListSets request.

        :rtype: :class:`~sickle.app.OAIResponse`
        """
        params = kwargs
        params.update({'verb': 'GetRecord'})
        response = self.harvest(**params)
        return OAIResponse(response, params, self)

    def ListMetadataFormats(self, **kwargs):
        """Issue a ListMetadataFormats request.

        :rtype: :class:`~sickle.app.OAIResponse`
        """
        params = kwargs
        params.update({'verb': 'ListMetadataFormats'})
        response = self.harvest(**params)
        return OAIResponse(response, params, self)


class OAIResponse(object):
    """A response from an OAI server.

    Provides access to the returned data on different abstraction
    levels::

        >>> response = sickle.ListRecords(metadataPrefix='oai_dc')
        >>> response.xml
        <Element {http://www.openarchives.org/OAI/2.0/}OAI-PMH at 0x10469a8c0>
        >>> response.raw
        u'<?xml version=\'1.0\' encoding ...'

    :param response: The original HTTP response.
    :param params: The OAI parameters for the request.
    :type params: dict
    :param sickle: The Sickle object that issued the original request.
    :type sickle: :class:`~sickle.app.Sickle`
    """
    def __init__(self, response, params, sickle):
        self.params = params
        self.response = response
        self.sickle = sickle

    @property
    def raw(self):
        """The server's response as unicode."""
        return self.response.text

    @property
    def xml(self):
        """The server's response as parsed XML."""
        return etree.XML(self.response.text.encode("utf8"))

    def iter(self, convert=None):
        """Iterate through the resulting records of the request.

        Iterable OAI verbs are:
            - ListRecords
            - ListIdentifiers
            - ListSets


         Raises NotImplementedError if called on a response for a non-eligible OAI request
         (e.g., Identify).

        :rtype: :class:`sickle.app.OAIIterator`
        """
        if self.params.get("verb") not in ['ListRecords', 'ListSets', 'ListIdentifiers']:
            raise NotImplementedError(
                '%s can not be iterated' % self.params.get("verb"))
        else:
            return OAIIterator(self, self.sickle, convert=convert)

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
    def __init__(self, oai_response, sickle, convert=None, ignore_deleted=False):
        self.sickle = sickle
        self.oai_response = oai_response
        self.verb = self.oai_response.params.get("verb")

        # Determine on what element to iterate (records, headers, or sets)
        if self.verb == 'ListRecords':
            self.element = 'record'
        elif self.verb == 'ListIdentifiers':
            self.element = 'header'
        elif self.verb == 'ListSets':
            self.element = 'set'
        self.convert = convert
        self.ignore_deleted = ignore_deleted
        self.record_list = self._get_records()
        self.resumption_token = self._get_resumption_token()
        self.request = getattr(self.sickle, self.verb)

    def __iter__(self):
        return self

    def __repr__(self):
        return '<OAIIterator %s>' % self.verb

    def _is_deleted(self, record):
        """Return True if a record/header is deleted, False otherwise.

        :param record: XML element.
        :rtype: bool
        """
        if self.element == 'record':
            header = record.find('.//' + self.sickle.oai_namespace + 'header')
        elif self.element == 'header':
            # work on header element directly in case of ListIdentifiers
            header = record
        else:
            # sets cannot be deleted
            return False
        if header.attrib.get('status') == 'deleted':
            return True
        else:
            return False

    def _get_resumption_token(self):
        """Extract the resumptionToken from the OAI response."""
        resumption_token = self.oai_response.xml.find(
            './/' + self.sickle.oai_namespace + 'resumptionToken')
        if resumption_token is None:
            return None
        else:
            return resumption_token.text

    def _get_records(self):
        """Extract records/headers/sets from the OAI response."""
        records = self.oai_response.xml.findall(
            './/' + self.sickle.oai_namespace + self.element)
        if self.ignore_deleted:
            records = [record for record in records
                       if not self._is_deleted(record)]
        return records

    def _next_batch(self):
        """Get the next response from the OAI server."""
        while self.record_list == []:
            self.oai_response = self.request(
                resumptionToken=self.resumption_token)
            self.record_list = self._get_records()
            self.resumption_token = self._get_resumption_token()
            if self.record_list == [] and self.resumption_token is None:
                raise StopIteration

    def next(self):
        """Return the next record/header/set."""
        if (not self.record_list and self.resumption_token is None):
            raise StopIteration
        elif len(self.record_list) == 0:
            self._next_batch()
        current_record = self.record_list.pop()
        if self.convert:
            return self.convert(current_record)
        else:
            return current_record


class Header(object):
    """Represents an OAI Header."""
    def __init__(self, header_element, strip_ns=True):
        self._header_element = header_element
        self._strip_ns = strip_ns
        self._oai_namespace = get_namespace(self._header_element)
        
        self.identifier = self._header_element.find(self._oai_namespace + 'identifier').text
        self.datestamp = self._header_element.find(self._oai_namespace + 'datestamp').text
        self.setSpecs = [setSpec.text for setSpec in 
                self._header_element.findall(self._oai_namespace + 'setSpec')]
        
    def __repr__(self):
        return '<Header %s>' % self.identifier



class Record(object):
    """Represents an OAI record."""
    def __init__(self, record_element, strip_ns=True):
        super(Record, self).__init__()
        self._record_element = record_element
        self._strip_ns = strip_ns
        self._oai_namespace = get_namespace(self._record_element)
        self.header = xml_to_dict(self._record_element.getchildren()[0], 
                        strip_ns=True)
        self.metadata = xml_to_dict(self._record_element.getchildren()[1],
                         strip_ns=self._strip_ns)

    def __repr__(self):
        return '<Record %s>' % self.header['identifier'][0]


