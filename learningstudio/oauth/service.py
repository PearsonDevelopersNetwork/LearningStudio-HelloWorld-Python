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
service
-------

Defines services for generating OAuth request signatures.


"""

import time
import uuid
import base64
import copy
import json

PY_3 = False

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus
    PY_3 = True

from learningstudio.oauth.request import OAuth1Request, OAuth2Request
from learningstudio.oauth.util import gen_authcode, current_time_millis
from learningstudio.oauth.util import parse_url, url_query_to_dict
from learningstudio.oauth.util import parse_url_and_connect, json_loads
from learningstudio.oauth.config import consumer_key, application_id
from learningstudio.oauth.config import consumer_secret, application_name
from learningstudio.oauth.config import client_string

class AuthMethod:
    """Defines constants that identify the exact type of an OAuthService object.

    The constants are exposed as return values of functions to prevent unintentional
    mutation.

    """
    __OAUTH1_SIGNATURE_SERVICE = 0
    __OAUTH2_PASSWORD_SERVICE = 1
    __OAUTH2_ASSERTION_SERVICE = 2

    @staticmethod 
    def oauth1_signature_service(): return AuthMethod.__OAUTH1_SIGNATURE_SERVICE

    @staticmethod
    def oauth2_password_service(): return AuthMethod.__OAUTH2_PASSWORD_SERVICE

    @staticmethod
    def oauth2_assertion_service(): return AuthMethod.__OAUTH2_ASSERTION_SERVICE

class OAuthServiceFactory:
    """Factory for building various OAuthService objects.

    """
    def __init__(self, configuration):
        """Initializes a OAuthServiceFactory object.

        :param configuration: The configuration used for building the OAuthService object.
        :type configuration: dict

        """
        self.__configuration = configuration

    def build(self, name):
        """Builds and returns an OAuthService object. 

        :param name: The type of the object to create.
        :type name: str
        :returns: An OAuthService object.
    
        """
        if name == AuthMethod.oauth1_signature_service(): return OAuth1SignatureService(self.__configuration)
        elif name == AuthMethod.oauth2_password_service(): return OAuth2PasswordService(self.__configuration)
        elif name == AuthMethod.oauth2_assertion_service(): return OAuth2AssertionService(self.__configuration)
        else: raise NotImplementedError(name)

class OAuth1SignatureService:
    """Generates an OAuth1 signature service request.

    """
 
    SIGNATURE_METHOD = 'CMAC-AES'

    def __init__(self, configuration):
        """Initializes an OAuth1SignatureService object.

        :param configuration: The configuration used for initializing the service.
        :type configuration: dict

        """
        self.__configuration = configuration

    def generateRequest(self, http_method = 'GET',
                        url = None, body = None):
        """Creates and returns a signature that can be used with an OAuth1 request.

        :param http_method: HTTP method to be used in the request. Defaults to 'GET'.
        :type http_method: str
        :param url: The request URL.
        :type url: str
        :param body: The request content. Defaults to None.
        :type body: str
        :returns: A properly initialized OAuth1 request object.
        :rtype: :class:`learningstudio.oauth.request.OAuth1Request`

        """
        key = consumer_key(self.__configuration)
        appid = application_id(self.__configuration)
        oauth_params = { 'oauth_consumer_key' : key,
                         'application_id' : appid,
                         'oauth_signature_method' : OAuth1SignatureService.SIGNATURE_METHOD,
                         'oauth_timestamp' : OAuth1SignatureService.__get_timestamp(),
                         'oauth_nonce' : OAuth1SignatureService.__get_nonce() }
        body = body.encode(encoding = 'UTF-8') if OAuth1SignatureService.__method_has_body(http_method) and (type(body) is str) else None
        secret = consumer_secret(self.__configuration)
        oauth_params['oauth_signature'] = OAuth1SignatureService.__gensign(http_method, url, 
                                                                           oauth_params, body,                                                    
                                                                           secret)
        sign = OAuth1SignatureService.__make_signature(oauth_params)
        return OAuth1Request(headers = OAuth1SignatureService.__make_headers(url, sign),
                             signature = sign)

    @staticmethod
    def __method_has_body(http_method):
        return http_method == 'POST' or http_method == 'PUT'

    @staticmethod
    def __make_headers(url, sign):
        i = url.find('?')
        if i > 0: url = url[:i]
        return { 'X-Authorization' : 'OAuth realm="%s",%s' % (url, sign) }
        
    @staticmethod
    def __make_signature(oauth_params):
        s = ''
        for key in oauth_params.keys():
            value = oauth_params[key]
            s += '%s="%s",' % (key, quote_plus(value))
        return s[:-1]

    @staticmethod
    def __get_timestamp():
        return str(int(round(time.time())))

    @staticmethod
    def __get_nonce():
        return str(uuid.uuid4().hex.upper()[0:32])

    @staticmethod
    def __gensign(http_method, url, oauth_params, body_bytes, secret):
        http_method = http_method.upper()
        encoded_params = OAuth1SignatureService.__normalize_params(http_method, url, 
                                                                   oauth_params, body_bytes)
        encoded_uri = quote_plus(parse_url(url).path)
        return OAuth1SignatureService.__gencmac(secret, '%s&%s&%s' % (http_method, 
                                                                      encoded_uri,
                                                                      encoded_params))

    @staticmethod
    def __normalize_params(http_method, url, oauth_params, body_bytes):
        oauth_params = copy.deepcopy(oauth_params)
        qdict = url_query_to_dict(parse_url(url).query)
        for key in qdict.keys():
            value = qdict[key]
            if isinstance(value, list): value = value[0]
            oauth_params[str(key)] = str(value)
        if body_bytes != None:
            if type(body_bytes) is bytes: body_bytes = body_bytes.decode(encoding = 'UTF-8')
            data = body_bytes.replace('\r\n', '')
            if PY_3: body_bytes = base64.b64encode(data.encode(encoding = 'UTF-8')).decode(encoding = 'UTF-8')
            else: body_bytes = base64.b64encode(data)
            oauth_params['body'] = quote_plus(quote_plus(body_bytes))

        combined_params = ''
        for key in sorted(oauth_params, key = str.lower):
            combined_params += '%s=%s&' % (key, oauth_params[key])

        return quote_plus(combined_params[:-1])
        
    @staticmethod
    def __gencmac(key, msg):
        return gen_authcode(key, msg)

OAUTH_API_DOMAIN = 'https://api.learningstudio.com'
OAUTH_URL = OAUTH_API_DOMAIN + '/token'

OAUTH_TIMESTAMP_FMT = '%Y-%m-%dT%H:%M:%SZ'

def build_assertion(application_name, consumer_key,
                    application_id, client_string, username,
                    consumer_secret):
    timestamp = time.strftime(OAUTH_TIMESTAMP_FMT, time.gmtime())
    assertion = '%s|%s|%s|%s|%s|%s' % (application_name, consumer_key, application_id,
                                       client_string, username, timestamp)
    cmac = gen_authcode(consumer_secret, assertion, b64 = False)
    return '%s|%s' % (assertion, cmac)

def make_oauth2request(url, data):
    byte_array = data.encode(encoding = 'UTF-8') if type(data) is str else data
    http_conn = None    
    try:
        http_conn, parts = parse_url_and_connect(url)
        headers = { 'Content-Type' : 'application/x-www-form-urlencoded',
                    'Content-Length' : len(byte_array) }
        http_conn.request('POST', parts.path, byte_array, headers)
        response = http_conn.getresponse()
        data = response.read()
        json_data = json_loads(data)
        return json_to_oauth2request(json_data)
    finally:
        if http_conn != None:
            http_conn.close()
    return None

def json_to_oauth2request(json_data):
    access_token = json_data.get('access_token')
    if (access_token == None or len(access_token) == 0):
        raise IOError('Missing access token.')
    creation_time = current_time_millis()
    authstr = 'Access_Token access_token=%s' % (access_token,)
    headers = {'X-Authorization' : authstr.encode(encoding = 'UTF-8') if type(authstr) is str else authstr}
    return OAuth2Request(headers = headers,
                         access_token = access_token,
                         expires_in_seconds = json_data.get('expires_in', 0),
                         refresh_token = json_data.get('refresh_token'),
                         creation_time = creation_time)

class OAuth2PasswordService:
    """Generates an OAuth2 password service request.

    """

    GRANT_TYPE = 'password'
    
    def __init__(self, configuration):
        """Initializes an OAuth2PasswordService object.

        :param configuration: The configuration required by the OAuth2PasswordService object.
        :type configuration: dict

        """
        self.__configuration = configuration

    def generateRequest(self, username = None, password = None):
        """Creates and returns a signature that can be used with a OAuth2 request with a password grant-type.

        :param username: The username required for authentication.
        :type username: str
        :param password: The password required for authentication.
        :type password: str
        :returns: An object that represents an OAuth2 signature.
        :rtype: class:`learningstudio.oauth.request.OAuth2Request`

        """
        uname = quote_plus(client_string(self.__configuration) + '\\' + username)
        data = 'grant_type=%s&client_id=%s&username=%s&password=%s' % (OAuth2PasswordService.GRANT_TYPE,
                                                                       quote_plus(application_id(self.__configuration)),
                                                                       uname,
                                                                       quote_plus(password))
        return make_oauth2request(OAUTH_URL, data)

    def refreshOAuth2PasswordRequest(self, last_request):
        """Refreshes the OAuth2 signature.

        :param last_request: The signature generated by the last call to :func:`learningstudio.oauth.service.OAuth2PasswordService.generateRequest` or :func:`learningstudio.oauth.service.OAuth2PasswordService.refreshOAuth2PasswordRequest`.
        :type last_request: OAuth2Request
        :returns: A newly generated signature.
        :rtype: :class:`learningstudio.oauth.request.OAuth2Request`

        """
        grant_type = 'refresh_token'
        appid = application_id(self.__configuration)
        data = 'grant_type=%s&client_id=%s&refresh_token=%s' % (grant_type,
                                                                appid,
                                                                last_request.getRefreshToken(),)
        return make_oauth2request(OAUTH_URL, data)

class OAuth2AssertionService:
    """Generates an Oauth2 Assertion service request.

    """

    GRANT_TYPE = 'assertion'
    ASSERTION_TYPE = 'urn:ecollege:names:moauth:1.0:assertion'

    def __init__(self, configuration):
        """Initializes a new OAuth2AssertionService object.

        :param configuration: The configuration required by the new object.
        :type configuration: dict
        
        """
        self.__configuration = configuration

    def generateRequest(self, username = None):
        """Creates and returns a signature that can be used with an OAuth2 request with the assertion grant-type.

        :param username: The username required for authentication.
        :type username: str
        :returns: An object that represents an OAuth2 assertion request signature.
        :rtype: :class:`learningstudio.oauth.request.OAuth2Request`

        """
        assertion = build_assertion(application_name(self.__configuration), 
                                    consumer_key(self.__configuration),
                                    application_id(self.__configuration), 
                                    client_string(self.__configuration),
                                    username,
                                    consumer_secret(self.__configuration))
        data = 'grant_type=%s&assertion_type=%s&assertion=%s' % (OAuth2AssertionService.GRANT_TYPE,
                                                                 quote_plus(OAuth2AssertionService.ASSERTION_TYPE),
                                                                 quote_plus(assertion))
        return make_oauth2request(OAUTH_URL, data)
