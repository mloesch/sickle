==============
Testing Sickle
==============


Sickle is tested against static OAI responses stored in files.
To this end, a mock version of the :meth:`sickle.app.Sickle.harvest`
method is created that reads the stored responses.

.. autofunction:: sickle.tests.test_sickle.fake_harvest



