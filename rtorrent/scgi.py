#!/usr/bin/env python
# 
# Copyright (C) 2012 W. Trevor King <wking@drexel.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import socket as _socket
import sys as _sys
try:  # Python 3
    import urllib.parse as _urllib_parse
except ImportError:  # Python 2
    import urlparse as _urllib_parse


__version__ = '0.1'


def get_socket(args):
    """Open a socket specified by the command line arguments.

    This could be extended to support Unix sockets.
    """
    return _socket.create_connection((args.host, args.port))

def netstring(string):
    """Convert a string into a netstring.

    >>> netstring('hello world!')
    '12:hello world!,'
    """
    return '{}:{},'.format(len(string), string)

def header(method, uri, data=None):
    """Return the content string of an SCGI header."""
    try:
        content_length = len(data)
    except TypeError:
        content_length = 0
    # From RFC 2616, section 5.1.2:
    #   REQUEST_URI is hex-encoded absolute path
    # From Nginx HttpCoreModule docs:
    #   $document_uri
    #     The same as $uri.
    #   $request_uri
    #     This variable is equal to the *original* request URI as
    #     received from the client including the args. It cannot be
    #     modified. Look at $uri for the post-rewrite/altered
    #     URI. Does not include host name. Example:
    #     "/foo/bar.php?arg=baz"
    #  $uri
    #     This variable is the current request URI, without any
    #     arguments (see $args for those). This variable will reflect
    #     any modifications done so far by internal redirects or the
    #     index module. Note this may be different from $request_uri,
    #     as $request_uri is what was originally sent by the browser
    #     before any such modifications. Does not include the protocol
    #     or host name. Example: /foo/bar.html
    scheme,netloc,path,params,query,fragment = _urllib_parse.urlparse(uri)
    # <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    scheme = netloc = ''
    request_uri = _urllib_parse.urlunparse(
        (scheme, netloc, path, params, query, fragment))
    document_uri = path
    strings = [
        'CONTENT_LENGTH\x00{}\x00'.format(content_length),
        'SCGI\x00{}\x00'.format(1),
        'REQUEST_METHOD\x00{}\x00'.format(method),
        'REQUEST_URI\x00{}\x00'.format(request_uri),
        'DOCUMENT_URI\x00{}\x00'.format(document_uri),
        ]
    return ''.join(strings)

def recvall(socket):
    """Recieve all data from a socket until it closes."""
    ret = []
    while True:
        r = socket.recv(1024)
        if not r:
            break
        ret.append(r)
    return b''.join(ret)

def request(socket, data=None, **kwargs):
    """Send a request and return the response string."""
    ns = netstring(header(data=data, **kwargs))
    if _sys.version_info >= (3, 0):  # Python 3
        ns = ns.encode('ascii')
    socket.sendall(ns)
    if data:
        socket.sendall(data)    
    return recvall(socket)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--host', default='localhost', help='hostname')
    parser.add_argument(
        '-p', '--port', default=5000, type=int, help='port number')
    parser.add_argument(
        '-m', '--method', default='GET', help='request method')
    parser.add_argument(
        '-d', '--data',  default='', help='request data')
    parser.add_argument(
        'uri', help='request URI')

    args = parser.parse_args()

    socket = get_socket(args)
    response = None
    response = request(socket=socket, method=args.method, uri=args.uri, data=args.data.encode('utf8'))
    socket.close()
    if response:
        if _sys.version_info >= (3, 0):  # Python 3
            sys.stdout.buffer.write(response)
        else:
            sys.stdout.write(response)
