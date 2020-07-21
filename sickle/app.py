# coding: utf-8
"""
    sickle.app
    ~~~~~~~~~~

    An OAI-PMH client.

    :copyright: Copyright 2015 Mathias Loesch
"""
import inspect
import logging
import time

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from sickle.iterator import BaseOAIIterator, OAIItemIterator
from sickle.response import OAIResponse
from .models import (Set, Record, Header, MetadataFormat,
                     Identify)

logger = logging.getLogger(__name__)

OAI_NAMESPACE = '{http://www.openarchives.org/OAI/%s/}'


# Map OAI verbs to class representations
DEFAULT_CLASS_MAP = {
    'GetRecord': Record,
    'ListRecords': Record,
    'ListIdentifiers': Header,
    'ListSets': Set,
    'ListMetadataFormats': MetadataFormat,
    'Identify': Identify,
}


class Sickle(object):
    """Client for harvesting OAI interfaces.

    Use it like this::

        >>> sickle = Sickle('http://elis.da.ulcc.ac.uk/cgi/oai2')
        >>> records = sickle.ListRecords(metadataPrefix='oai_dc')
        >>> records.next()
        <Record oai:eprints.rclis.org:3780>

    :param endpoint: The endpoint of the OAI interface.
    :type endpoint: str
    :param http_method: Method used for requests (GET or POST, default: GET).
    :type http_method: str
    :param protocol_version: The OAI protocol version.
    :type protocol_version: str
    :param iterator: The type of the returned iterator
           (default: :class:`sickle.iterator.OAIItemIterator`)
    :param max_retries: Number of retry attempts if an HTTP request fails (default: 0 = request only once). Sickle will
                        use the value from the retry-after header (if present) and will wait the specified number of
                        seconds between retries.
    :type max_retries: int
    :param retry_status_codes: HTTP status codes to retry (default will retry on 429, 500, 502, 503 and 504)
    :type retry_status_codes: iterable
    :param retry_backoff_factor: Backoff factor to apply between retries after the second try,
                                 if no Retry-After header is sent by the server. Default: 1.5
    :type retry_backoff_factor: float
    :type protocol_version: str
    :param class_mapping: A dictionary that maps OAI verbs to classes representing
                          OAI items. If not provided,
                          :data:`sickle.app.DEFAULT_CLASS_MAPPING` will be used.
    :type class_mapping: dict
    :param encoding:     Can be used to override the encoding used when decoding
                         the server response. If not specified, `requests` will
                         use the encoding returned by the server in the
                         `content-type` header. However, if the `charset`
                         information is missing, `requests` will fallback to
                         `'ISO-8859-1'`.
    :type encoding:      str
    :param request_args: Arguments to be passed to requests when issuing HTTP
                         requests. Useful examples are `auth=('username', 'password')`
                         for basic auth-protected endpoints or `timeout=<int>`.
                         See the `documentation of requests <http://docs.python-requests.org/en/master/api/#main-interface>`_
                         for all available parameters.
    """

    def __init__(self, endpoint,
                 http_method='GET',
                 protocol_version='2.0',
                 iterator=OAIItemIterator,
                 max_retries=0,
                 retry_status_codes=None,
                 default_retry_after=None,
                 retry_backoff_factor=1.5,
                 class_mapping=None,
                 encoding=None,
                 **request_args):

        self.endpoint = endpoint
        if http_method not in ['GET', 'POST']:
            raise ValueError("Invalid HTTP method: %s! Must be GET or POST.")
        if protocol_version not in ['2.0', '1.0']:
            raise ValueError(
                "Invalid protocol version: %s! Must be 1.0 or 2.0.")
        self.http_method = http_method
        self.protocol_version = protocol_version
        if inspect.isclass(iterator) and issubclass(iterator, BaseOAIIterator):
            self.iterator = iterator
        else:
            raise TypeError(
                "Argument 'iterator' must be subclass of %s" % BaseOAIIterator.__name__)

        if default_retry_after is not None:
            logger.warning("default_retry_after is no longer supported, please use retry_backoff_factor instead.")

        retry_adapter = requests.adapters.HTTPAdapter(max_retries=Retry(
            total=max_retries,
            backoff_factor=retry_backoff_factor,
            status_forcelist=retry_status_codes or [429, 500, 502, 503, 504],
            method_whitelist=['GET', 'POST']
        ))
        self.session = requests.Session()
        self.session.mount('https://', retry_adapter)
        self.session.mount('http://', retry_adapter)

        self.oai_namespace = OAI_NAMESPACE % self.protocol_version
        self.class_mapping = class_mapping or DEFAULT_CLASS_MAP
        self.encoding = encoding
        self.request_args = request_args

    def harvest(self, **kwargs):  # pragma: no cover
        """Make HTTP requests to the OAI server.

        :param kwargs: OAI HTTP parameters.
        :rtype: :class:`sickle.OAIResponse`
        """
        http_response = self._request(kwargs)
        if self.encoding:
            http_response.encoding = self.encoding
        return OAIResponse(http_response, params=kwargs)

    def _request(self, kwargs):
        if self.http_method == 'GET':
            response = self.session.get(self.endpoint, params=kwargs, **self.request_args)
        response = self.session.post(self.endpoint, data=kwargs, **self.request_args)
        response.raise_for_status()
        return response

    def ListRecords(self, ignore_deleted=False, **kwargs):
        """Issue a ListRecords request.

        :param ignore_deleted: If set to :obj:`True`, the resulting
                              iterator will skip records flagged as deleted.
        :rtype: :class:`sickle.iterator.BaseOAIIterator`
        """
        params = kwargs
        params.update({'verb': 'ListRecords'})
        # noinspection PyCallingNonCallable
        return self.iterator(self, params, ignore_deleted=ignore_deleted)

    def ListIdentifiers(self, ignore_deleted=False, **kwargs):
        """Issue a ListIdentifiers request.

        :param ignore_deleted: If set to :obj:`True`, the resulting
                              iterator will skip records flagged as deleted.
        :rtype: :class:`sickle.iterator.BaseOAIIterator`
        """
        params = kwargs
        params.update({'verb': 'ListIdentifiers'})
        return self.iterator(self,
                             params, ignore_deleted=ignore_deleted)

    def ListSets(self, **kwargs):
        """Issue a ListSets request.

        :rtype: :class:`sickle.iterator.BaseOAIIterator`
        """
        params = kwargs
        params.update({'verb': 'ListSets'})
        return self.iterator(self, params)

    def Identify(self):
        """Issue an Identify request.

        :rtype: :class:`sickle.models.Identify`
        """
        params = {'verb': 'Identify'}
        return Identify(self.harvest(**params))

    def GetRecord(self, **kwargs):
        """Issue a ListSets request."""
        params = kwargs
        params.update({'verb': 'GetRecord'})
        record = self.iterator(self, params).next()
        return record

    def ListMetadataFormats(self, **kwargs):
        """Issue a ListMetadataFormats request.

        :rtype: :class:`sickle.iterator.BaseOAIIterator`
        """
        params = kwargs
        params.update({'verb': 'ListMetadataFormats'})
        return self.iterator(self, params)

    def get_retry_after(self, http_response):
        if http_response.status_code == 503:
            try:
                return int(http_response.headers.get('retry-after'))
            except TypeError:
                return self.default_retry_after
        return self.default_retry_after

    @staticmethod
    def _is_error_code(status_code):
        return status_code >= 400
