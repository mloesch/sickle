Sickle: An OAI Client Library for Python
========================================


Sickle is an OAI-PMH client library written in Python.  It has been designed
to provide different levels of abstraction when communicating with OAI-PMH
interfaces::

    >>> sickle = Sickle('http://elis.da.ulcc.ac.uk/cgi/oai2')
    >>> records = sickle.ListRecords(metadataPrefix='oai_dc')


Most importantly, Sickle lets you convienently iterate through resumption batches
without having to deal with ``resumptionTokens`` yourself::
    >>> records.next()
    <Record ...>


Requirements
============

* requests (mandatory)
* lxml (recommended for performance)


