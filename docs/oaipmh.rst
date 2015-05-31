==============
OAI-PMH Primer
==============

This section gives a basic overview of the
`Open Archives Protocol for Metadata Harvesting (OAI-PMH) <http://openarchives.org>`_.
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

OAI interfaces may expose metadata records in multiple metadata formats. These
formats are identified by so-called "metadata prefixes". For instance, the
prefix ``oai_dc`` refers to the OAI-DC format, which by definition has to be
exposed by every valid OAI interface. OAI-DC is based on the 15 metadata
elements specified in the
`Dublin Core Metadata Element Set <http://dublincore.org/documents/dces/>`_.


.. note::

    Sickle only supports the OAI-DC format out of the box. See the section
    on :ref:`customizing <customizing>` for information on how to extend
    Sickle for retrieving metadata in other formats.
