# coding: utf-8
"""
    sickle.iterator
    ~~~~~~~~~~~~~~~

    Collects classes for iterating over OAI responses

    :copyright: Copyright 2015 Mathias Loesch
"""

from sickle import oaiexceptions
from sickle.models import ResumptionToken


# Map OAI verbs to the XML elements
VERBS_ELEMENTS = {
    'GetRecord': 'record',
    'ListRecords': 'record',
    'ListIdentifiers': 'header',
    'ListSets': 'set',
    'ListMetadataFormats': 'metadataFormat',
    'Identify': 'Identify',
}


class BaseOAIIterator(object):
    """Iterator over OAI records/identifiers/sets transparently aggregated via
    OAI-PMH.

    Can be used to conveniently iterate through the records of a repository.

    :param sickle: The Sickle object that issued the first request.
    :type sickle: :class:`sickle.app.Sickle`
    :param params: The OAI arguments.
    :type params:  dict
    :param ignore_deleted: Flag for whether to ignore deleted records.
    :type ignore_deleted: bool
    """

    def __init__(self, sickle, params, ignore_deleted=False):
        self.sickle = sickle
        self.params = params
        self.ignore_deleted = ignore_deleted
        self.verb = self.params.get('verb')
        self.resumption_token = None
        self._next_response()

    def __iter__(self):
        return self

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.verb)

    def _get_resumption_token(self):
        """Extract and store the resumptionToken from the last response."""
        resumption_token_element = self.oai_response.xml.find(
            './/' + self.sickle.oai_namespace + 'resumptionToken')
        if resumption_token_element is None:
            return None
        token = resumption_token_element.text
        cursor = resumption_token_element.attrib.get('cursor', None)
        complete_list_size = resumption_token_element.attrib.get(
            'completeListSize', None)
        expiration_date = resumption_token_element.attrib.get(
            'expirationDate', None)
        resumption_token = ResumptionToken(
            token=token, cursor=cursor,
            complete_list_size=complete_list_size,
            expiration_date=expiration_date
        )
        return resumption_token

    def _next_response(self):
        """Get the next response from the OAI server."""
        params = self.params
        if self.resumption_token:
            params = {
                'resumptionToken': self.resumption_token.token,
                'verb': self.verb
            }
        self.oai_response = self.sickle.harvest(**params)
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
        self.resumption_token = self._get_resumption_token()

    def next(self):
        """Must be implemented by subclasses."""
        raise NotImplementedError


class OAIResponseIterator(BaseOAIIterator):
    """Iterator over OAI responses."""

    def next(self):
        """Return the next response."""
        while True:
            if self.oai_response:
                response = self.oai_response
                self.oai_response = None
                return response
            elif self.resumption_token:
                self._next_response()
            else:
                raise StopIteration


class OAIItemIterator(BaseOAIIterator):
    """Iterator over OAI records/identifiers/sets transparently aggregated via
    OAI-PMH.

    Can be used to conveniently iterate through the records of a repository.

    :param sickle: The Sickle object that issued the first request.
    :type sickle: :class:`sickle.app.Sickle`
    :param params: The OAI arguments.
    :type params:  dict
    :param ignore_deleted: Flag for whether to ignore deleted records.
    :type ignore_deleted: bool
    """

    def __init__(self, sickle, params, ignore_deleted=False):
        self.mapper = sickle.class_mapping[params.get('verb')]
        self.element = VERBS_ELEMENTS[params.get('verb')]
        super(OAIItemIterator, self).__init__(sickle, params, ignore_deleted)

    def _next_response(self):
        super(OAIItemIterator, self)._next_response()
        self._items = self.oai_response.xml.iterfind(
            './/' + self.sickle.oai_namespace + self.element)

    def next(self):
        """Return the next record/header/set."""
        while True:
            for item in self._items:
                mapped = self.mapper(item)
                if self.ignore_deleted and mapped.deleted:
                    continue
                return mapped
            if self.resumption_token:
                self._next_response()
            else:
                raise StopIteration
