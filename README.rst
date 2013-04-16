Sickle: An OAI Client Library for Python
========================================


Sickle is an OAI-PMH client library written in Python::

    >>> sickle = Sickle('http://elis.da.ulcc.ac.uk/cgi/oai2')
    >>> records = sickle.ListRecords(metadataPrefix='oai_dc')


Most importantly, Sickle lets you conveniently iterate through resumption batches
without having to deal with ``resumptionTokens`` yourself::
    >>> records.next()
    <Record ...>


Installation
============

::

    pip install sickle

Dependencies:

* `requests <http://docs.python-requests.org/en/latest/>`_
* `lxml <http://lxml.de/>`_


