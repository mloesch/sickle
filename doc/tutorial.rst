========
Tutorial
========

This section gives a brief overview on how to use Sickle for querying OAI
interfaces.


OAI-PMH Primer
==============

This section gives a basic overview of
the `Open Archives Protocol for Metadata Harvesting (OAI-PMH) <http://openarchives.org>`_.
For more detailed information, please refer to the protocol specification.

Glossary of Important OAI-PMH Concepts
--------------------------------------

**Repository**
    A *repository* is a server-side application that exposes metadata via OAI-PMH.
**Harvester**
    OAI-PMH client applications like Sickle are called *harvesters*.
**record**
    A *record* is the XML-encoded container for the metadata of a single publication item.
    It consists of a *header* and a *metadata* section.
**header**
    The record *header* contains a unique identifier and a datestamp.
**metadata**
    The record *metadata* contains the publication metadata in a defined
    metadata format.
**set**
    A structure for grouping records for selective harvesting.
**harvesting**
    The process of requesting records from the repository by the harvester.

OAI Verbs
---------

OAI-PMH  features six main API methods (so-called "OAI verbs") that can be issued by
harvesters. Some verbs can be combined with further arguments:

``Identify``
    Returns information about the repository. Arguments: None.
``GetRecord``
    Returns a single record. Arguments:

    * ``identifier`` (the unique identifier of the record, *required*)
    * ``metadataPrefix`` (the prefix identifying the metadata format, *required*)
``ListRecords``
    Returns the records in the repository in batches (possibly filtered by a timestamp or a ``set``).
    Arguments:

    * ``metadataPrefix`` (the prefix identifying the metadata format, *required*)
    * ``from`` (the earliest timestamp of the records, *optional*)
    * ``until`` (the latest timestamp of the records, *optional*)
    * ``set`` (a set for selective harvesting, *optional*)
    * ``resumptionToken`` (used for getting the next result batch if the number of records returned by the previous request exceeds the repository's maximum batch size, *exclusive*)
``ListIdentifiers``
    *Like* ``ListRecords`` *but returns only the record headers.*
``ListSets``
    Returns the list of sets supported by this repository.
    Arguments: None
``ListMetadataFormats``
    Returns the list of metadata formats supported by this repository.
    Arguments: None


Metadata Formats
----------------

OAI interfaces may expose metadata records in multiple metadata formats. These formats
are identified by so-called "metadata prefixes". For instance, the prefix ``oai_dc`` refers
to the OAI-DC format, which by definition has to be exposed by every valid OAI interface.
OAI-DC is based on the 15 metadata elements specified in the
`Dublin Core Metadata Element Set <http://dublincore.org/documents/dces/>`_.

.. note::

    Sickle only supports the OAI-DC format out of the box. See section XXX for
    how to extend Sickle for retrieving metadata in other formats.


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


Getting a Single Record
=======================

OAI-PMH allows you to get a single record by using the ``GetRecord`` verb. And so does Sickle:

    >>> sickle.GetRecord(identifier='oai:eprints.rclis.org:4088',
    ...            metadataPrefix='oai_dc')
    <Record oai:eprints.rclis.org:4088>


Ignoring Deleted Records
========================

The :meth:`~sickle.app.Sickle.ListRecords` and :meth:`~sickle.app.Sickle.ListIdentifiers`
methods take an optional parameter :attr:`ignore_deleted`. If it is set to :obj:`True`,
the returned :class:`~sickle.app.OAIIterator` will skip deleted records/headers::

    >>> records = sickle.ListRecords(metadataPrefix='oai_dc',
    ...                ignore_deleted=True)



