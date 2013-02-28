============================
Customizing the Item Classes
============================

Sickle provides Python representations for all OAI-specific items.
However, although it works fine with Dublin-Core-encoded metadata
payloads, the :class:`sickle.models.Record` class implementation 
may not be compatible with all metadata formats out there.

In this case you can write your own reflection classes by subclassing
the default implementations. Then you need to implement the XML unpacking 
yourself by overriding the :meth:`unpack` method::

    from sickle.models import Record

    class MyRecord(Record):
        def unpack(self, xml):
            # Your XML unpacking implementation goes here.
            # 
            return {...}

Next, associate your implementation with OAI verbs in the :class:`~sickle.app.Sickle` object.
In this case, we want the :class:`~sickle.app.Sickle` object to
use our implementation to unpack ListRecords and GetRecord responses::

    sickle = Sickle('http://...')
    sickle.class_mapping['ListRecords'] = MyRecord
    sickle.class_mapping['GetRecord'] = MyRecord

If you need to rewrite *all* item implementations, you can also provide a
complete mapping to the :class:`~sickle.app.Sickle` object at
instantiation::

    my_mapping = {
        'ListRecords': MyRecord,
        'GetRecord': MyRecord,
        ...
    }

    sickle = Sickle('http://...', class_mapping=my_mapping)