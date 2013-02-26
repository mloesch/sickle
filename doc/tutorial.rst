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

    >>> records = sickle.ListRecords(metadataPrefix='oai_dc')

Note that all keyword arguments you provide to this function are passed to the OAI interface 
as HTTP parameters. Therefore our example request results in ``verb=ListRecords&metadataPrefix=oai_dc``.
Consequently, we can add additional parameters, like ``set`` for example::

    >>> records = sickle.ListRecords(metadataPrefix='oai_dc', set='driver')


Using the ``from`` Parameter
============================

If you need to perform selective harvesting by date using the ``from`` parameter, you
will run into problems though, since ``from`` is a reserved word in Python::

    >>> records = sickle.ListRecords(metadataPrefix='oai_dc', from="2012-12-12")
      File "<stdin>", line 1
        records = sickle.ListRecords(metadataPrefix='oai_dc', from="2012-12-12")
                                                                  ^
    SyntaxError: invalid syntax

Fortunately, you can circumvent this problem by using a dictionary together with 
the ``**`` operator::
    
    >>> records = sickle.ListRecords(
    ...     **{'metadataPrefix': 'oai_dc',
    ...       'from': '2012-12-12'
    ...       }
    ... )


Iterative Harvesting
====================

Sickle lets you conveniently iterate through resumption batches
without having to deal with ``resumptionTokens`` yourself::

    >>> records = sickle.ListRecords(metadataPrefix='oai_dc')
    >>> records.next()
    <Record oai:eprints.rclis.org:4088>

Note that this works with all requests that return more than one element.
These are: :meth:`~sickle.app.Sickle.ListRecords`, :meth:`~sickle.app.Sickle.ListIdentifiers`, 
:meth:`~sickle.app.Sickle.ListSets`, and :meth:`~sickle.app.Sickle.ListMetadataFormats`.

Iterating through the headers returned by ``ListIdentifiers``::

    >>> headers = sickle.ListIdentifiers(metadataPrefix='oai_dc')
    >>> headers.next()
    <Header oai:eprints.rclis.org:4088>

Or through the sets returned by ``ListSets``::
    
    >>> sets = sickle.ListSets()
    >>> sets.next()
    <Set Status = In Press>


Ignoring Deleted Records
========================

The :meth:`~sickle.app.Sickle.ListRecords` and :meth:`~sickle.app.Sickle.ListIdentifiers` 
methods take an optional parameter :attr:`ignore_deleted`. If it is set to :obj:`True`,
the returned :class:`~sickle.app.OAIIterator` will skip deleted records/headers::

    >>> records = sickle.ListRecords(metadataPrefix='oai_dc', 
                    ignore_deleted=True)



