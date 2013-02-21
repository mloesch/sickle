========
Tutorial
========

This section gives a brief overview of how to use Sickle .


Initialize an OAI Interface
===========================

To make a connection to an OAI interface, you need to import the Sickle object::

    >>> from sickle import Sickle

Next, you can initialize the connection by passing it the basic URL. In our
example, we use the OAI interface of the ELIS repository::

    >>> sickle = Sickle('http://elis.da.ulcc.ac.uk/cgi/oai2')


Issuing Requests
================

Now you are set to issue some requests. Sickle provides methods for each of
the six OAI verbs (ListRecords, GetRecord, Idenitfy, ListSets, ListMetadataFormats, 
ListIdentifiers). Start with a ListRecords request::

    >>> response = sickle.ListRecords(metadataPrefix='oai_dc')

Note that all keyword arguments you provide to this function are passed to the OAI interface 
as HTTP parameters. Therefore our example request results in ``verb=ListRecords&metadataPrefix=oai_dc``.
Consequently, we can add additional parameters, like ``set`` for example::

    >>> response = sickle.ListRecords(metadataPrefix='oai_dc', set='driver')


Using the ``from`` Parameter
============================

If you need to perform selective harvesting by date using the ``from`` parameter, you
will run into problems though, since ``from`` is a reserved word in Python::

    >>> response = sickle.ListRecords(metadataPrefix='oai_dc', from="2012-12-12")
      File "<stdin>", line 1
        response = sickle.ListRecords(metadataPrefix='oai_dc', from="2012-12-12")
                                                                  ^
    SyntaxError: invalid syntax

Fortunately, you can circumvent this problem by using a dictionary together with 
the ``**`` operator::
    
    >>> response = sickle.ListRecords(
    ...     **{'metadataPrefix': 'oai_dc',
    ...       'from': '2012-12-12'
    ...       }
    ... )



Dealing with Responses
======================

In most cases, you will work with the parsed XML responses::
    
    >>> response.xml
    <Element {http://www.openarchives.org/OAI/2.0/}OAI-PMH at 0x10469a8c0>

But you can also access the raw response for debugging::

    >>> response.raw
    u'<?xml version=\'1.0\' encoding ...'

This is especially useful if you want to access OAI interfaces with broken XML.  


Iterative Harvesting
====================

Sickle lets you convienently iterate through resumption batches
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
