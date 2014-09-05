"""
LearningStudio HelloWorld Application & API Explorer 

Need Help or Have Questions? 
Please use the PDN Developer Community at https://community.pdn.pearson.com

:category   LearningStudio HelloWorld
:author     Wes Williams <wes.williams@pearson.com>
:author     Pearson Developer Services Team <apisupport@pearson.com>
:copyright  2014 Pearson Education Inc.
:license    http://www.apache.org/licenses/LICENSE-2.0  Apache 2.0
:version    1.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""
util
----

Utility functions. Functions that takes care of Py2 and Py3 compatibility issues also goes here.


"""

import os
import time
import datetime
import ctypes
import copy
import json
import xml.etree.ElementTree as ET
from dateutil import parser

try:
    from httplib import HTTPConnection, HTTPSConnection
except ImportError:
    from http.client import HTTPConnection, HTTPSConnection

try:
    from urlparse import urlparse, parse_qs, ParseResult
except ImportError:
    from urllib.parse import urlparse, parse_qs, ParseResult

authcode_lib = None

if os.name == 'posix':
    authcode_lib = ctypes.cdll.LoadLibrary('pyauthcode.so')
else:
    authcode_lib = ctypes.windll.LoadLibrary('pyauthcode')

if authcode_lib == None:
    raise RuntimeError('Failed to load pyauthcode shared library.')

authcode_lib.gen_authcode.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int,)
authcode_lib.gen_authcode.restype = ctypes.c_void_p

authcode_lib.free_authcode.argtypes = (ctypes.c_void_p,)
authcode_lib.free_authcode.restype = None

def current_time_millis():
    """Returns the current system time milliseconds.

    :returns: The current system time in milliseconds.
    :rtype: long

    """
    return int(round(time.time() * 1000))

def unix_time(dt):
    """Returns the time based on the Unix epoch - Thursday, 1 January 1970.

    :returns: Time based on seconds elapsed since the Unix epoch.
    :rtype: datetime
    
    """
    epoch = datetime.datetime.utcfromtimestamp(0)
    dt = dt.replace(tzinfo = None)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    """Returns the milliseconds elapsed since the Unix epoch.

    :returns: The milliseconds elapsed since the Unix epoch.
    :rtype: long

    """
    return unix_time(dt) * 1000.0

def gen_authcode(key, msg, b64 = True):
    """Generates the authentication code by calling the CMAC implementation in the crypto++ wrapper.
    
    :param key: The 32-byte authentication key used for encoding.
    :type key: str
    :param msg: The message that needs to be encoded.
    :type msg: str
    :param b64: A flag that indicates whether the generated code needs to be Base-64 encoded or not. Defaults to `True`.
    :type b64: bool

    :returns: Encoded `msg`.
    :rtype: str

    """
    if type(key) is str: key = key.encode(encoding = 'UTF-8')
    if type(msg) is str: msg = msg.encode(encoding = 'UTF-8')
    out = authcode_lib.gen_authcode(ctypes.c_char_p(key), ctypes.c_char_p(msg), b64)
    result = copy.deepcopy(ctypes.string_at(out))
    if type(result) is bytes: result = result.decode(encoding = 'UTF-8')
    authcode_lib.free_authcode(out)
    return result.replace('\n', '')

def free_authcode(authcode):
    authcode_lib.free_authcode(authcode)

def parse_url(url):
    return urlparse(url)

def parts_to_url(scheme, netloc, path, params, 
                 query, fragment):
    p = ParseResult(scheme, netloc, path,
                    params, query, fragment)
    return p.geturl()

def url_query_to_dict(query):
    return parse_qs(query)

def parse_url_and_connect(url):
    url_parts = urlparse(url)
    use_ssl = url_parts.scheme == 'https'
    host = url_parts.netloc
    return (HTTPSConnection(host) if use_ssl else HTTPConnection(host),
            url_parts)

def parse_xml_tag(xml, tags):
    root = ET.fromstring(xml)
    if root.tag == tags[0]:
        tags = tags[1:]
    while (True):
        children = root.findall(tags[0])
        if children == None: return None
        if len(tags) == 1: 
            return children[0].text
        else: 
            root = children[0]
            tags = tags[1:]

def datetime_to_millis(time_value):
    """Converts a datetime object to milliseconds since the Unix epoch.
    
    :param time_value: The datetime object to convert.
    :type time_value: datetime

    :returns: Milliseconds representation of `time_value`.
    :rtype: long

    """
    dt = parser.parse(time_value + '+0000')
    return unix_time_millis(dt)

def add_delay():
    time.sleep(3)

def json_loads(data):
    if type(data) is bytes: data = data.decode(encoding = 'UTF-8')
    return json.loads(data)

