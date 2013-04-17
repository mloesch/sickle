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


Installation
============

::

    pip install sickle

Dependencies:

* `requests <http://docs.python-requests.org/en/latest/>`_
* `lxml <http://lxml.de/>`_


Links
=====

* `Documentation <https://sickle.readthedocs.org/en/latest/>`_
* `Sickle @ GitHub <https://github.com/mloesch/sickle>`_