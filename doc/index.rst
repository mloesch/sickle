.. Sickle documentation master file, created by
   sphinx-quickstart on Mon Feb 18 14:10:13 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================================
Sickle: An OAI Client Library for Python
========================================

Sickle is lightweight `OAI-PMH <http://www.openarchives.org/OAI/openarchivesprotocol.html>`_
client library written in Python.  It has been designed for conveniently retrieving
data from OAI interfaces the Pythonic way::

    >>> sickle = Sickle('http://elis.da.ulcc.ac.uk/cgi/oai2')
    >>> records = sickle.ListRecords(metadataPrefix='oai_dc')

Most importantly, Sickle lets you iterate through OAI records without having to deal
with things like result batches or ``resumptionTokens`` yourself::

    >>> records.next()
    <Record oai:eprints.rclis.org:4088>

Sickle maps the OAI records to Python objects::

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

Important Links
===============

* `Sickle @ PyPI <https://pypi.python.org/pypi/Sickle>`_
* `Sickle @ GitHub <https://github.com/mloesch/sickle>`_

Table of Contents
=================

.. toctree::
   :maxdepth: 2

   installation
   tutorial
   api
   customizing
   development
   credits

