# -*- coding: utf-8 -*-

#   __
#  /__)  _  _     _   _ _/   _
# / (   (- (/ (/ (- _)  /  _)
#          /

"""
Requests HTTP Library
~~~~~~~~~~~~~~~~~~~~~

Requests is an HTTP library, written in Python, for human beings. Basic GET
usage:

   >>> import requests
   >>> r = requests.get('https://www.python.org')
   >>> r.status_code
   200
   >>> 'Python is a programming language' in r.content
   True

... or POST:

   >>> payload = dict(key1='value1', key2='value2')
   >>> r = requests.post('http://httpbin.org/post', data=payload)
   >>> print(r.text)
   {
     ...
     "form": {
       "key2": "value2",
       "key1": "value1"
     },
     ...
   }

The other HTTP methods are supported - see `requests.api`. Full documentation
is at <http://python-requests.org>.

:copyright: (c) 2017 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""

from .__about__ import (
    title as __title__,
    version as __version__,
    build as __build__,
    author as __author__,
    license as __license__,
    copyright as __copyright__,
    cake as __cake__,
)

# Attempt to enable urllib3's SNI support, if possible
try:
    from .packages.urllib3.contrib import pyopenssl
    pyopenssl.inject_into_urllib3()
except ImportError:
    pass

import warnings

# urllib3's DependencyWarnings should be silenced.
from .packages.urllib3.exceptions import DependencyWarning
warnings.simplefilter('ignore', DependencyWarning)

from . import utils
from .models import Request, Response, PreparedRequest
from .api import request, get, head, post, patch, put, delete, options
from .sessions import session, Session
from .status_codes import codes
from .exceptions import (
    RequestException, Timeout, URLRequired,
    TooManyRedirects, HTTPError, ConnectionError,
    FileModeWarning, ConnectTimeout, ReadTimeout
)

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

# FileModeWarnings go off per the default.
warnings.simplefilter('default', FileModeWarning, append=True)
