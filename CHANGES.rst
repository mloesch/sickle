Changelog
=========

Version 0.6.5
-------------

January 12, 2020

- fix: repr methods where causing an exception on Python 3 (https://github.com/mloesch/sickle/issues/30)



Version 0.6.4
-------------

October 2, 2018

- fix: resumption token with empty body indicates last response (https://github.com/mloesch/sickle/issues/25)



Version 0.6.3
-------------

April 8, 2018

- fix unicode problems (issues 20 & 22)


Version 0.6.2
-------------

August 11, 2017

- missing datestamp and identifier elements in record header don't break harvesting
- lxml resolve_entities disabled (http://lxml.de/FAQ.html#how-do-i-use-lxml-safely-as-a-web-service-endpoint)


Version 0.6.1
-------------

November 13, 2016

- it is now possible to pass any keyword arguments to requests
- the encoding used to decode the server response can be overridden


Version 0.5
-----------

November 12, 2015

- support for Python 3
- consider resumption tokens with empty tag bodies


Version 0.4
-----------

May 31, 2015

- bug fix: resumptionToken parameter is exclusive
- added support for harvesting complete OAI-XML responses


Version 0.3
-----------

April 17, 2013

- added support for protected OAI interfaces (basic authentication)
- made class mapping for OAI elements configurable
- added options for HTTP timeout and max retries
- added handling of HTTP 503 responses


Version 0.2
-----------

February 26, 2013

- OAI items are now represented as their own classes instead of XML elements
- library raises OAI-specific exceptions
- made lxml a required dependency


Version 0.1
-----------

February 20, 2013

First public release.
