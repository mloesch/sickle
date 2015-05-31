# coding: utf-8
"""
    sickle.models
    ~~~~~~~~~~~~~

    Collects classes for OAI-specific entities.

    :copyright: Copyright 2015 Mathias Loesch
"""

from lxml import etree

from .utils import get_namespace, xml_to_dict


class ResumptionToken(object):
    """Represents a resumption token."""

    def __init__(self, token='', cursor='', complete_list_size='',
                 expiration_date=''):
        self.token = token
        self.cursor = cursor
        self.complete_list_size = complete_list_size
        self.expiration_date = expiration_date

    def __repr__(self):
        return '<ResumptionToken %s>' % self.token


class OAIItem(object):
    """A generic OAI item.

    :param xml: XML representation of the entity.
    :param strip_ns: Flag for whether to remove the namespaces from the
                     element names in the dictionary representation.
    """

    def __init__(self, xml, strip_ns=True):
        super(OAIItem, self).__init__()

        #: The original parsed XML
        self.xml = xml
        self._strip_ns = strip_ns
        self._oai_namespace = get_namespace(self.xml)

    def __str__(self):
        return etree.tounicode(self.xml).encode("utf8")

    def __unicode__(self):
        return etree.tounicode(self.xml)

    @property
    def raw(self):
        """The original XML as unicode."""
        return etree.tounicode(self.xml)


class Identify(OAIItem):
    """Represents an Identify container.

    This object differs from the other entities in that is has to be created
    from a :class:`sickle.response.OAIResponse` instead of an XML element.

    :param identify_response: The response for an Identify request.
    :type identify_response: :class:`sickle.OAIResponse`
    """

    def __init__(self, identify_response):
        super(Identify, self).__init__(identify_response.xml, strip_ns=True)
        self.xml = self.xml.find('.//' + self._oai_namespace + 'Identify')
        self._identify_dict = xml_to_dict(self.xml, strip_ns=True)
        for k, v in self._identify_dict.items():
            setattr(self, k.replace('-', '_'), v[0])

    def __repr__(self):
        return '<Identify>'

    def __iter__(self):
        return self._identify_dict.iteritems()


class Header(OAIItem):
    """Represents an OAI Header.

    :param header_element: The XML element 'header'.
    :type header_element: :class:`lxml.etree._Element
    """

    def __init__(self, header_element):
        super(Header, self).__init__(header_element, strip_ns=True)
        self.deleted = self.xml.attrib.get('status') == 'deleted'
        self.identifier = self.xml.find(
            self._oai_namespace + 'identifier').text
        self.datestamp = self.xml.find(
            self._oai_namespace + 'datestamp').text
        self.setSpecs = [setSpec.text for setSpec in
                         self.xml.findall(self._oai_namespace + 'setSpec')]

    def __repr__(self):
        if self.deleted:
            return '<Header %s [deleted]>' % self.identifier
        else:
            return '<Header %s>' % self.identifier

    def __iter__(self):
        return iter([
            ('identifier', self.identifier),
            ('datestamp', self.datestamp),
            ('setSpecs', self.setSpecs)
        ])


class Record(OAIItem):
    """Represents an OAI record.

    :param record_element: The XML element 'record'.
    :type record_element: :class:`lxml.etree._Element`
    :param strip_ns: Flag for whether to remove the namespaces from the
                     element names.
    """

    def __init__(self, record_element, strip_ns=True):
        super(Record, self).__init__(record_element, strip_ns=strip_ns)
        self.header = Header(self.xml.find(
            './/' + self._oai_namespace + 'header'))
        self.deleted = self.header.deleted
        if not self.deleted:
            # We want to get record/metadata/<container>/*
            # <container> would be the element ``dc``
            # in the ``oai_dc`` case.
            self.metadata = xml_to_dict(
                self.xml.find(
                    './/' + self._oai_namespace + 'metadata'
                ).getchildren()[0], strip_ns=self._strip_ns)

    def __repr__(self):
        if self.header.deleted:
            return '<Record %s [deleted]>' % self.header.identifier
        else:
            return '<Record %s>' % self.header.identifier

    def __iter__(self):
        return self.metadata.iteritems()


class Set(OAIItem):
    """Represents an OAI set.

    :param set_element: The XML element 'set'.
    :type set_element: :class:`lxml.etree._Element
    """

    def __init__(self, set_element):
        super(Set, self).__init__(set_element, strip_ns=True)
        self._set_dict = xml_to_dict(self.xml, strip_ns=True)
        for k, v in self._set_dict.items():
            setattr(self, k.replace('-', '_'), v[0])

    def __repr__(self):
        return u'<Set %s>'.encode('utf8') % self.setName

    def __iter__(self):
        return self._set_dict.iteritems()


class MetadataFormat(OAIItem):
    """Represents an OAI MetadataFormat.

    :param mdf_element: The XML element 'metadataFormat'.
    :type mdf_element: :class:`lxml.etree._Element
    """

    def __init__(self, mdf_element):
        super(MetadataFormat, self).__init__(mdf_element, strip_ns=True)
        #: The prefix of this format.
        self._mdf_dict = xml_to_dict(self.xml, strip_ns=True)
        for k, v in self._mdf_dict.items():
            setattr(self, k.replace('-', '_'), v[0])

    def __repr__(self):
        return u'<MetadataFormat %s>'.encode('utf8') % self.metadataPrefix

    def __iter__(self):
        return self._mdf_dict.iteritems()
