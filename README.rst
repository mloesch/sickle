Sickle: OAI-PMH for Humans
==========================

.. image:: https://travis-ci.org/mloesch/sickle.svg?branch=master
    :target: https://travis-ci.org/mloesch/sickle
.. image:: https://img.shields.io/pypi/v/Sickle.svg
    :target: https://pypi.python.org/pypi/Sickle
.. image:: https://img.shields.io/pypi/dm/sickle.svg
        :target: https://pypi.python.org/pypi/Sickle

Sickle is a lightweight `OAI-PMH <http://www.openarchives.org/OAI/openarchivesprotocol.html>`_
client library written in Python.  It has been designed for conveniently retrieving data from
OAI interfaces the Pythonic way::

    >>> from sickle import Sickle
    >>> sickle = Sickle('http://elis.da.ulcc.ac.uk/cgi/oai2')
    >>> records = sickle.ListRecords(metadataPrefix='oai_dc')
    >>> records.next()
    <Record oai:eprints.rclis.org:4088>

Features
--------

- Easy harvesting of OAI-compliant interfaces
- Support for all six OAI verbs
- Convenient object representations of OAI items (records, headers, sets, ...)
- Automatic de-serialization of Dublin Core-encoded metadata payloads to Python
  dictionaries
- Option for ignoring deleted items

Installation
------------

::

    pip install sickle

Dependencies:

* `requests <http://docs.python-requests.org/en/latest/>`_
* `lxml <http://lxml.de/>`_


Documentation
-------------

Documentation is available at `Read the Docs <https://sickle.readthedocs.org/en/latest/>`_

Development
-----------

* `Sickle @ GitHub <https://github.com/mloesch/sickle>`_
