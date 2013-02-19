Sickle: An OAI Client Library for Python
========================================


Sickle is an OAI-PMH client library written in Python.  It has been designed
to provide different levels of abstraction when communicating with OAI-PMH
interfaces::

    >>> sickle = Sickle('http://elis.da.ulcc.ac.uk/cgi/oai2')
    >>> response = sickle.ListRecords(metadataPrefix='oai_dc')

Sickle provides access to the parsed XML for convenience::
    
    >>> response.xml
    <Element {http://www.openarchives.org/OAI/2.0/}OAI-PMH at 0x10469a8c0>

But also to the raw response for debugging::

    >>> response.raw
    u'<?xml version=\'1.0\' encoding ...'


This is especially useful if you want to access OAI interfaces with broken XML.
Most importantly, Sickle lets you convienently iterate through resumption batches
without having to deal with ``resumptionTokens`` yourself::

    >>> response = sickle.ListRecords(metadataPrefix='oai_dc')
    >>> records = response.iter()
    >>> records.next()
    <Element {http://www.openarchives.org/OAI/2.0/}record at 0x1051b3b90>

Note that this works with all requests that support the resumptionToken parameter.
Like for iterating through the headers returned by ``ListIdentifiers``::

    >>> response = sickle.ListIdentifiers(metadataPrefix='oai_dc')
    >>> headers = response.iter()
    >>> headers.next()
    <Element {http://www.openarchives.org/OAI/2.0/}header at 0x1051b1c30>

Or through the sets returned by ``ListSets``::
    
    >>> response = sickle.ListSets()
    >>> sets = response.iter()
    >>> sets.next()
    <Element {http://www.openarchives.org/OAI/2.0/}set at 0x1051b6cd0>

Requirements
============

* requests (mandatory)
* lxml (recommended for performance)


