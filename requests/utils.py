# -*- coding: utf-8 -*-

"""
requests.utils
~~~~~~~~~~~~~~

This module provides utlity functions that are used within Requests
that are also useful for external consumption.

"""

import cgi
import cookielib
import re
import zlib


def header_expand(header_dict):
    """Returns an HTTP Header value string from a dictionary.

    Example expansion::

        # Accept: text/x-dvi; q=.8; mxb=100000; mxt=5.0, text/x-c
        {'text/x-dvi': {'q': '.8', 'mxb': '100000', 'mxt': '5.0'}, 'text/x-c': {}}
    """

    collector = []

    for i, (value, params) in enumerate(header_dict.items()):
        _params = []

        for p_k, p_v in params.items():

            _params.append('{k}={v}'.format(k=p_k, v=p_v))

        if len(params):
            collector.append(value)
            collector.append('; ')
            collector.append('; '.join(_params))

            if not len(header_dict) == i+1:
                collector.append(', ')

    return ''.join(collector)



def dict_from_cookiejar(cj):
    """Returns a key/value dictionary from a CookieJar.

    :param cj: CookieJar object to extract cookies from.
    """

    cookie_dict = {}

    for _, cookies in cj._cookies.items():
        for _, cookies in cookies.items():
            for cookie in cookies.values():
                # print cookie
                cookie_dict[cookie.name] = cookie.value

    return cookie_dict


def cookiejar_from_dict(cookie_dict):
    """Returns a CookieJar from a key/value dictionary.

    :param cookie_dict: Dict of key/values to insert into CookieJar.
    """

    # return cookiejar if one was passed in
    if isinstance(cookie_dict, cookielib.CookieJar):
        return cookie_dict

    # create cookiejar
    cj = cookielib.CookieJar()

    cj = add_dict_to_cookiejar(cj, cookie_dict)

    return cj


def add_dict_to_cookiejar(cj, cookie_dict):
    """Returns a CookieJar from a key/value dictionary.

    :param cj: CookieJar to insert cookies into.
    :param cookie_dict: Dict of key/values to insert into CookieJar.
    """

    for k, v in cookie_dict.items():

        cookie = cookielib.Cookie(
            version=0,
            name=k,
            value=v,
            port=None,
            port_specified=False,
            domain='',
            domain_specified=False,
            domain_initial_dot=False,
            path='/',
            path_specified=True,
            secure=False,
            expires=None,
            discard=True,
            comment=None,
            comment_url=None,
            rest={'HttpOnly': None},
            rfc2109=False
        )

        # add cookie to cookiejar
        cj.set_cookie(cookie)

    return cj


def get_encodings_from_content(content):
    """Returns encodings from given content string.

    :param content: bytestring to extract encodings from.
    """

    charset_re = re.compile(r'<meta.*?charset=["\']*(.+?)["\'>]', flags=re.I)

    return charset_re.findall(content)


def get_encoding_from_headers(headers):
    """Returns encodings from given HTTP Header Dict.

    :param headers: dictionary to extract encoding from.
    """

    content_type = headers.get('content-type')
    content_type, params = cgi.parse_header(content_type)

    if 'charset' in params:
        return params['charset'].strip("'\"")


def unicode_from_html(content):
    """Attempts to decode an HTML string into unicode.
    If unsuccessful, the original content is returned.
    """

    encodings = get_encodings_from_content(content)

    for encoding in encodings:

        try:
            return unicode(content, encoding)
        except (UnicodeError, TypeError):
            pass

        return content


def get_unicode_from_response(r):
    """Returns the requested content back in unicode.

    :param r: Reponse object to get unicode content from.

    Tried:

    1. charset from content-type

    2. every encodings from ``<meta ... charset=XXX>``

    3. fall back and replace all unicode characters

    """

    tried_encodings = []

    # Try charset from content-type
    encoding = get_encoding_from_headers(r.headers)

    if encoding:
        try:
            return unicode(r.content, encoding)
        except UnicodeError:
            tried_encodings.append(encoding)

    # Fall back:
    try:
        return unicode(r.content, encoding, errors='replace')
    except TypeError:
        return r.content


def decode_gzip(content):
    """Return gzip-decoded string.

    :param content: bytestring to gzip-decode.
    """

    return zlib.decompress(content, 16+zlib.MAX_WBITS)


def curl_from_request(request):
    """Creates a curl command from the request."""

    #TODO - OAuth

    #: -L/--location - if there is a redirect, redo request on the new place
    curl = 'curl -L '

    #: -u/--user - Specify the user name and password to use for server auth.
    #: Basic Auth only for now
    auth = ''
    if request.auth is not None:
       auth = '-u "%s:%s" ' % (request.auth.username, request.auth.password)

    method = ''
    if request.method.upper() == 'HEAD':
        #: -I/--head - fetch headers only
        method = '-I '
    else:
        #: -X/--request - specify request method
        method = '-X %s ' % request.method.upper()

    #: -b/--cookie
    #: (HTTP) Pass the data to the HTTP server as a cookie. It is supposedly the
    #: data previously received from the server in a "Set-Cookie:" line.
    cookies = ''
    if request.cookiejar:
        cookies = cookies.join(['-b "%s=%s" ' % (k.name, k.value) for k in request.cookiejar])

    #: -H/--header - Extra header to use when getting a web page
    header = ''
    if request.headers:
        header = header.join(['-H "%s:%s" ' % (k, v) for k, v in request.headers.iteritems()])

    form = ''
    if request.method in ('PUT', 'POST', 'PATCH'):
        #: request.files is updated with request.data if both exist.
        #: ContentType multipart/form-data is used
        if request.files:
           #: -F/--form - Emulate form data. To force 'content' to a file, prefix file name @.
            for k, v in request.files.iteritems():
                if isinstance(v, file):
                    form = form + '-F "%s=@%s" ' % (k, v.name)
                elif v not in (None, ''):
                    form = form + '-F "%s=%s" ' % (k, v)

        #: content-type application/x-www-form-urlencoded is used here
        else:
            #: -d/--data - send specified data in post request.
            if isinstance(request.data, (list, tuple)):
                form = form.join(['-d "%s=%s" ' % (k, v) for k, v in request.data])
            elif request._enc_data not in (None, ''):
                form = "-d '%s' " % (request._enc_data)

    #: Params handled in _build_url
    return curl + auth + method + header + cookies + form + '"' + request._build_url() + '"'

