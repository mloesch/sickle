===
API
===

The Sickle Client
=================


.. autoclass:: sickle.app.Sickle
    :members:

    .. attribute:: last_response

        Contains the last response that has been received.



Working with OAI Responses
==========================

.. autoclass:: sickle.response.OAIResponse
    :members:


Iterating over OAI Items
========================


.. autoclass:: sickle.iterator.OAIItemIterator
    :members:

    .. attribute oai_response

        The last response from the OAI server.

    .. attribute:: sickle

        The :class:`sickle.app.Sickle` instance used for making requests to the server.

    .. attribute:: verb

        The OAI verb used for making requests to the server.

    .. attribute:: element

        The name of the OAI item to iterate on (``record``, ``header``, ``set`` or
        ``metadataFormat``).

    .. attribute:: resumption_token

        The content of the XML element ``resumptionToken`` from the last request.

    .. attribute:: ignore_deleted

        Flag for whether to skip records marked as deleted.



Iterating over OAI Responses
============================


.. autoclass:: sickle.iterator.OAIResponseIterator
    :members:



Classes for OAI Items
=====================

The following classes represent OAI-specific items like records, headers, and sets.
All items feature the attributes :attr:`raw` and :attr:`xml` which contain their
original XML representation as unicode and as parsed XML objects.

.. note::

    Sickle's automatic mapping of XML to OAI objects only works for Dublin Core
    encoded record data.

Identify Object
---------------

The Identify object is generated from Identify responses and is returned by
:meth:`sickle.app.Sickle.Identify`.  It contains general information about
the repository.

.. autoclass:: sickle.models.Identify
    :members:
    :inherited-members:

    .. note::

        As the attributes of this class are auto-generated from the Identify XML elements,
        some of them may be missing for specific OAI interfaces.

    .. attribute:: adminEmail

        The content of the element ``adminEmail``. Normally the repository's administrative
        contact.

    .. attribute:: baseURL

        The content of the element ``baseURL``, which is the URL of the repository's OAI endpoint.

    .. attribute:: respositoryName

        The content of the element ``repositoryName``, which contains the name of the repository.

    .. attribute:: deletedRecord

        The content of the element ``deletedRecord``, which indicates whether and how the repository keeps track
        of deleted records.

    .. attribute:: delimiter

        The content of the element ``delimiter``.

    .. attribute:: description

        The content of the element ``description``, which contains a description of the repository.

    .. attribute:: earliestDatestamp

        The content of the element ``earliestDatestamp``, which indicates the datestamp of the oldest record
        in the repository.

    .. attribute:: granularity

        The content of the element ``granularity``, which indicates the granularity of the used dates.

    .. attribute:: oai_identifier

        The content of the element ``oai-identifier``.

        .. note:: ``oai-identifier`` is not a valid name in Python.

    .. attribute:: protocolVersion

        The content of the element ``protocolVersion``, which indicates the version of the OAI protocol
        implemented by the repository.

    .. attribute:: repositoryIdentifier

        The content of the element ``repositoryIdentifier``.

    .. attribute:: sampleIdentifier

        The content of the element ``sampleIdentifier``, which usually contains an example of an identifier
        used by this repository.

    .. attribute:: scheme

        The content of the element ``scheme``.

Record Object
-------------

Record objects represent single OAI records.

.. autoclass:: sickle.models.Record
    :members:
    :inherited-members:


    .. attribute:: header

        Contains the record header represented as a :class:`sickle.models.Header` object.

    .. attribute:: deleted

        A boolean flag that indicates whether this record is deleted.


Header Object
-------------

Header objects represent OAI headers.

.. autoclass:: sickle.models.Header
    :members:
    :inherited-members:


Set Object
----------

.. autoclass:: sickle.models.Set
    :members:
    :inherited-members:


    .. attribute:: setName

        The name of the set.

    .. attribute:: setSpec

        The identifier of this set used for querying.



MetadataFormat Object
---------------------

.. autoclass:: sickle.models.MetadataFormat
    :members:
    :inherited-members:

    .. attribute:: metadataPrefix

        The prefix used to identify this format.

    .. attribute:: metadataNamespace

        The namespace URL for this format.

    .. attribute:: schema

        The URL to the schema file of this format.
