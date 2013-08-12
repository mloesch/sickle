===========
Development
===========

Get the Code
------------

Sickle is developed on `GitHub <http://github.org/mloesch/sickle>`_.

Testing
-------

Sickle is tested with `nose <http://nose.readthedocs.org/en/latest/index.html>`_.

To run the tests, type:

.. code-block:: text

    python setup.py nosetests


Since the tests should not rely on an external OAI server, static OAI responses
stored in  files are used instead.  To this end, a mock version of  the
:meth:`sickle.app.Sickle.harvest` method is created that reads the stored
responses:

.. autofunction:: sickle.tests.test_sickle.fake_harvest



