# coding: utf-8
"""
    exceptions
    ~~~~~~~~~~

    OAI errors.

    :copyright: Copright 2013 Mathias Loesch
"""


class BadArgument(Exception):
    pass

class BadVerb(Exception):
    pass

class BadResumptionToken(Exception):
    pass

class CannotDisseminateFormat(Exception):
    pass

class IdDoesNotExist(Exception):
    pass

class NoSetHierarchy(Exception):
    pass

class NoMetadataFormat(Exception):
    pass

class NoRecordsMatch(Exception):
    pass

class OAIError(Exception):
    pass