.. _customizing:

=============================================
Harvesting other Metadata Formats than OAI-DC
=============================================

By default, Sickle's mapping of the record XML into Python
dictionaries is tailored to work only with Dublin-Core-encoded metadata
payloads. Other formats most probably won't be mapped correctly,
especially if they are more hierarchically structured than Dublin
Core.

In case your want to harvest these more complex formats, you have to
write your own record model class by subclassing the default
implementation that unpacks the metadata XML::

    from sickle.models import Record

    class MyRecord(Record):
        # Your XML unpacking implementation goes here.
        pass

.. note::

    Take a look at the implementation of :class:`sickle.models.Record`
    to get an idea of how to do this.

Next, associate your implementation with OAI verbs in the
:class:`~sickle.app.Sickle` object. In this case, we want the
:class:`~sickle.app.Sickle` object to use our implementation to represent
items returned by ListRecords and GetRecord responses::

    sickle = Sickle('http://...')
    sickle.class_mapping['ListRecords'] = MyRecord
    sickle.class_mapping['GetRecord'] = MyRecord

If you need to rewrite *all* item implementations, you can also provide a
complete mapping to the :class:`~sickle.app.Sickle` object at instantiation::

    my_mapping = {
        'ListRecords': MyRecord,
        'GetRecord': MyRecord,
        # ...
    }

    sickle = Sickle('http://...', class_mapping=my_mapping)
