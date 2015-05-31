# coding: utf-8
"""
    sickle.oaiexceptions
    ~~~~~~~~~~~~~~~~~~~~

    OAI errors.

    :copyright: Copyright 2015 Mathias Loesch
"""


class BadArgument(Exception):
    """
    The request includes illegal arguments, is missing required arguments,
    includes a repeated argument, or values for arguments have an illegal
    syntax.
    """
    pass


class BadVerb(Exception):
    """
    Value of the verb argument is not a legal OAI-PMH verb, the verb argument
    is missing, or the verb argument is repeated.
    """
    pass


class BadResumptionToken(Exception):
    """
    The value of the resumptionToken argument is invalid or expired.
    """
    pass


class CannotDisseminateFormat(Exception):
    """
    The metadata format identified by the value given for the metadataPrefix
    argument is not supported by the item or by the repository.
    """
    pass


class IdDoesNotExist(Exception):
    """
    The value of the identifier argument is unknown or illegal in this
    repository.
    """
    pass


class NoSetHierarchy(Exception):
    """
    The repository does not support sets.
    """
    pass


class NoMetadataFormat(Exception):
    """
    There are no metadata formats available for the specified item.
    """
    pass


class NoRecordsMatch(Exception):
    """
    The combination of the values of the from, until, set and metadataPrefix
    arguments results in an empty list.
    """
    pass


class OAIError(Exception):
    """
    Context specific OAI errors not covered by the classes above.
    """
    pass
