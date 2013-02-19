# coding: utf-8
"""
    Sickle
    ~~~~~~

    An OAI-PMH client.

    :copyright: Copright 2013 Mathias Loesch
"""


import sys
import os

import requests
try:
    from lxml import etree
except ImportError:
    from xml.etree import ElementTree as etree

from __init__ import __version__

OAI_NAMESPACE = '{http://www.openarchives.org/OAI/%s/}'

class Sickle(object):
    """OAI-PMH client."""
    def __init__(self, endpoint, http_method='GET', protocol_version='2.0'):
        super(Sickle, self).__init__()
        self.endpoint = endpoint
        self.http_method = http_method
        self.protocol_version = protocol_version
        self.oai_namespace = OAI_NAMESPACE % self.protocol_version
    
    def harvest(self, **kwargs):
        if self.http_method == 'GET':
            return requests.get(self.endpoint, params=kwargs)
        elif self.http_method == 'POST':
            return requests.post(self.endpoint, data=kwargs)

    def ListRecords(self, **kwargs):
        """Issue a ListRecords request."""
        params = kwargs
        params.update({'verb': 'ListRecords'})
        response = self.harvest(**params)
        return OAIResponse(response, params, self)

    def ListIdentifiers(self, **kwargs):
        """Issue a ListIdentifiers request."""
        params = kwargs
        params.update({'verb': 'ListIdentifiers'})
        response = self.harvest(**params)
        return OAIResponse(response, params, self)

    def ListSets(self, **kwargs):
        """Issue a ListSets request."""
        params = kwargs
        params.update({'verb': 'ListSets'})
        response = self.harvest(**params)
        return OAIResponse(response, params, self)

    def Identify(self):
        """Issue a ListSets request."""
        params = {'verb': 'Identify'}
        response = self.harvest(**params)
        return OAIResponse(response, params, self)

    def GetRecord(self, **kwargs):
        """Issue a ListSets request."""
        params = kwargs
        params.update({'verb': 'GetRecord'})
        response = self.harvest(**params)
        return OAIResponse(response, params, self)

    def ListMetadataFormats(self, **kwargs):
        """Issue a ListMetadataFormats request."""
        params = kwargs
        params.update({'verb': 'ListMetadataFormats'})
        response = self.harvest(**params)
        return OAIResponse(response, params, self)


class OAIResponse(object):
    """Represents a response from an OAI server.

    :param response: The original HTTP response.
    :param params: The OAI parameters for the request.
    :param sickle: The Sickle object that issued the request.
    """
    def __init__(self, response, params, sickle):
        self.params = params
        self.response = response
        self.sickle = sickle
    
    @property
    def raw(self):
        return self.response.text

    @property
    def xml(self):
        return etree.XML(self.response.text.encode("utf8"))

    def iter(self):
        if self.params.get("verb") not in ['ListRecords', 'ListSets', 'ListIdentifiers']:
            raise NotImplementedError, '%s can not be iterated' % self.params.get("verb")
        else:
            return OAIIterator(self, self.sickle)

    def __repr__(self):
        return '<OAIResponse %s>' % self.params.get('verb')


class OAIIterator(object):
    """Iterator over OAI records/identifiers/sets transparently aggregated via
    OAI-PMH.

    Can be used to conveniently iterate through the records of a repository::

        >>> response = sickle.ListRecords(metadataPrefix='oai_dc')
        >>> records = response.iter()
        >>> records.next()
        <Element {http://www.openarchives.org/OAI/2.0/}record at 0x1051b3b90>

    :param response: The first OAI response.
    :param sickle: The Sickle object that issued the first request.
    :param ignore_deleted: Flag for whether to ignore deleted records.
    """
    def __init__(self, response, sickle, ignore_deleted=False):
        self.sickle = sickle
        self.response = response
        self.verb = self.response.params.get("verb")

        if self.verb == 'ListRecords':
            self.element = 'record'
        elif self.verb == 'ListIdentifiers':
            self.element = 'header'
        elif self.verb == 'ListSets':
            self.element = 'set'
        self.ignore_deleted = ignore_deleted
        self.record_list = self._get_records(self.response)
        self.resumption_token = self._get_resumption_token(response)
        self.request = getattr(self.sickle, self.verb)

    def __iter__(self):
        return self

    def __repr__(self):
        return '<OAIIterator %s>' % self.verb

    def _is_deleted(self, record):
        if self.element == 'record':
            header = record.find('.//' + self.sickle.oai_namespace + 'header')
        elif self.element == 'header':
            # work on header element directly in case of ListIdentifiers
            header = record
        else:
            return False
        if header.attrib.get('status') == 'deleted':
            return True
        else:
            return False

    def _get_resumption_token(self, response):
        resumption_token = self.response.xml.find(
            './/' + self.sickle.oai_namespace + 'resumptionToken')
        if resumption_token is None:
            return None
        else:
            return resumption_token.text

    def _get_records(self, response):
        records = self.response.xml.findall(
            './/' + self.sickle.oai_namespace + self.element)
        if self.ignore_deleted:
            records = [record for record in records 
            if not self._is_deleted(record)]
        return records

    def _next_batch(self):
        while self.record_list == []:
            self.response = self.request(resumptionToken=self.resumption_token)
            self.record_list = self._get_records(self.response)
            self.resumption_token = self._get_resumption_token(self.response)
            if self.record_list == [] and self.resumption_token is None:
                raise StopIteration

    def next(self):
        if (not self.record_list and self.resumption_token is None):
            raise StopIteration
        elif len(self.record_list) == 0:
            self._next_batch()
        current_record = self.record_list.pop()
        return current_record

