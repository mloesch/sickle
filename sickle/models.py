# coding: utf-8
"""
    models
    ~~~~~~

    Collects classes for OAI-specific entities.

    :copyright: Copright 2013 Mathias Loesch
"""


from .utils import get_namespace, xml_to_dict


class Header(object):
    """Represents an OAI Header."""
    def __init__(self, header_element, strip_ns=True):
        self._header_element = header_element
        self._strip_ns = strip_ns
        self._oai_namespace = get_namespace(self._header_element)
        
        self.deleted = self._header_element.attrib.get('status') == 'deleted'
        self.identifier = self._header_element.find(self._oai_namespace + 'identifier').text
        self.datestamp = self._header_element.find(self._oai_namespace + 'datestamp').text
        self.setSpecs = [setSpec.text for setSpec in 
                self._header_element.findall(self._oai_namespace + 'setSpec')]
        
    def __repr__(self):
        if self.deleted:
            return '<Header %s [deleted]>' % self.identifier
        else:
            return '<Header %s>' % self.identifier

    @property
    def raw(self):
        return etree.tounicode(self._header_element)

    @property
    def xml(self):
        return self._header_element


class Record(object):
    """Represents an OAI record."""
    def __init__(self, record_element, strip_ns=True):
        super(Record, self).__init__()
        self._record_element = record_element
        self._strip_ns = strip_ns
        self._oai_namespace = get_namespace(self._record_element)
        self.header = Header(self._record_element.getchildren()[0], 
                        strip_ns=True)
        self.deleted = self.header.deleted
        if not self.deleted:
            self.metadata = xml_to_dict(self._record_element.getchildren()[1],
                         strip_ns=self._strip_ns)
        

    def __repr__(self):
        if self.header.deleted:
            return '<Record %s [deleted]>' % self.header.identifier
        else:
            return '<Record %s>' % self.header.identifier

    def __iter__(self):
        for k,v in self.metadata.items():
            yield (k, v)

    @property
    def raw(self):
        return etree.tounicode(self._record_element)

    @property
    def xml(self):
        return self._record_element


class Set(object):
    """Represents an OAI set."""
    def __init__(self, set_element, strip_ns=True):
        super(Set, self).__init__()
        self._set_element = set_element
        self._strip_ns = strip_ns
        self._oai_namespace = get_namespace(self._set_element)
        self.deleted = False
        self.setName = self._set_element.find(
                        self._oai_namespace + 'setName').text
        self.setSpec = self._set_element.find(
                        self._oai_namespace + 'setSpec').text

    def __repr__(self):
        return '<Set %s>' % self.setName

    def __iter__(self):
        return (setName, setSpec)

    @property
    def raw(self):
        return etree.tounicode(self._set_element)

    @property
    def xml(self):
        return self._set_element
