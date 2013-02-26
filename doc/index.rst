.. Sickle documentation master file, created by
   sphinx-quickstart on Mon Feb 18 14:10:13 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Sickle: An OAI Client Library for Python
========================================

.. toctree::
   :maxdepth: 2

   tutorial
   api

Sickle is lightweight OAI-PMH client library written in Python.  It has been designed
to provide different levels of abstraction when communicating with OAI-PMH
interfaces::

    >>> sickle = Sickle('http://elis.da.ulcc.ac.uk/cgi/oai2')
    >>> records = sickle.ListRecords(metadataPrefix='oai_dc')

Most importantly, Sickle lets you conveniently iterate through resumption batches
without having to deal with ``resumptionTokens`` yourself::

    >>> records.next()
    <Record oai:eprints.rclis.org:4088>

Sickle maps the OAI XML to Python objects::
  
    >>> record = records.next()
    >>> record.header
    <Header oai:eprints.rclis.org:4088>
    >>> record.header.identifier
    'oai:eprints.rclis.org:4088'

The metadata payload is stored as a dictionary::

    >>> record.metadata
    {'creator': ['Melloni, Marco'],
     'date': ['2000'],
     'description': [u'A web site for...