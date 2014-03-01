**************************
Sickle: OAI-PMH for Humans
**************************

Sickle is a lightweight `OAI-PMH <http://www.openarchives.org/OAI/openarchivesprotocol.html>`_
client library written in Python.  It has been designed for conveniently retrieving data from OAI interfaces the Pythonic way::

    >>> sickle = Sickle('http://elis.da.ulcc.ac.uk/cgi/oai2')
    >>> records = sickle.ListRecords(metadataPrefix='oai_dc')
    >>> records.next()
    <Record oai:eprints.rclis.org:4088>

Sickle maps all important OAI items to Python objects::

    >>> record.header
    <Header oai:eprints.rclis.org:4088>
    >>> record.header.identifier
    'oai:eprints.rclis.org:4088'

Dublin-Core-encoded metadata payloads are easily accessible as dictionaries::

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
   oaipmh
   api
   customizing
   development
   credits

