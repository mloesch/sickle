# coding: utf-8
"""
    models
    ~~~~~~

    Collects classes for OAI-specific entities.

    :copyright: Copright 2013 Mathias Loesch
"""

from .utils import get_namespace, xml_to_dict

from lxml import etree


class OAIEntity(object):
    """docstring for OAIEntity"""
    def __init__(self, xml, strip_ns=True):
        super(OAIEntity, self).__init__()
        self.xml = xml
        self._strip_ns = strip_ns
        self._oai_namespace = get_namespace(self.xml)
    
    def __str__(self):
        return etree.tounicode(self.xml).encode("utf8")

    def __unicode__(self):
        return etree.tounicode(self.xml)

    @property
    def raw(self):
        """The server's response as unicode."""
        return etree.tounicode(self.xml)
 

class Identify(OAIEntity):
    """docstring for Identify"""
    def __init__(self, identify_response):
        super(Identify, self).__init__(identify_response.xml, strip_ns=True)
        self.xml = self.xml.find('.//' + self._oai_namespace + 'Identify')
        self._identify_dict = xml_to_dict(self.xml, strip_ns=True)
        for k,v in self._identify_dict.items():
            setattr(self, k.replace('-', '_'), v[0])

    def __repr__(self):
        return '<Identify>'

    def __iter__(self):
        return self._identify_dict.iteritems()


class Header(OAIEntity):
    """Represents an OAI Header."""
    def __init__(self, header_element, strip_ns=True):
        super(Header, self).__init__(header_element, strip_ns=strip_ns)
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
        list_repr = [
            ('identifier', self.identifier), 
            ('datestamp', self.datestamp),
            ('setSpecs', self.setSpecs)
        ]
        for k, v in list_repr:
            yield k, v


class Record(OAIEntity):
    """Represents an OAI record."""
    def __init__(self, record_element, strip_ns=True):
        super(Record, self).__init__(record_element, strip_ns=strip_ns)
        
        self.header = Header(self.xml.find(
            './/' + self._oai_namespace + 'header'), strip_ns=True)
        self.deleted = self.header.deleted
        if not self.deleted:
            self.metadata = xml_to_dict(
                self.xml.find(
                    './/' + self._oai_namespace + 'metadata'
                ).getchildren()[0], strip_ns=True)

    def __repr__(self):
        if self.header.deleted:
            return '<Record %s [deleted]>' % self.header.identifier
        else:
            return '<Record %s>' % self.header.identifier

    def __iter__(self):
        for k, v in self.metadata.items():
            yield (k, v)


class Set(OAIEntity):
    """Represents an OAI set."""
    def __init__(self, set_element, strip_ns=True):
        super(Set, self).__init__(set_element, strip_ns=strip_ns)
        self.deleted = False
        self.setName = self.xml.find(
                        self._oai_namespace + 'setName').text
        self.setSpec = self.xml.find(
                        self._oai_namespace + 'setSpec').text

    def __repr__(self):
        return u'<Set %s>'.encode("utf8") % self.setName

    def __iter__(self):
        for element in [(self.setName, self.setSpec)]:
            yield element



class MetadataFormat(OAIEntity):
    """Represents an OAI MetadataFormat."""
    def __init__(self, mdf_element, strip_ns=True):
        super(MetadataFormat, self).__init__(mdf_element, strip_ns=strip_ns)
        self.deleted = False
        self.metadataPrefix = self.xml.find(
                        self._oai_namespace + 'metadataPrefix').text
        self.metadataNamespace = self.xml.find(
                        self._oai_namespace + 'metadataNamespace').text
        self.schema = self.xml.find(
                        self._oai_namespace + 'schema').text

    def __repr__(self):
        return u'<MetadataFormat %s>'.encode("utf8") % self.metadataPrefix

    def __iter__(self):
        return iter([
            ('metadataPrefix', self.metadataPrefix),
            ('schema', self.schema),
            ('namespace', self.metadataNamespace)
        ])
