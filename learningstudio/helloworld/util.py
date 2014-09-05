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
import logging

from learningstudio.oauth.util import parse_url_and_connect, json_loads

class Response:
    def __init__(self, 
                 status_code = 200, 
                 reason = 'OK',
                 content_type = 'text/json', 
                 content = None):
        self.__status_code = status_code
        self.__reason = reason
        self.__content_type = content_type
        self.__content = content

    def statusCode(self): return self.__status_code
    def reason(self): return self.__reason
    def contentType(self): return self.__content_type
    def content(self): return self.__content

def log_debug(s):
    logger = logging.getLogger('LearningStudio_HelloWorld')
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(s)

class LearningStudioUtility:
    @staticmethod 
    def doGet(uri, oauthHeaders): 
        return LearningStudioUtility.__doMethod('GET', uri, oauthHeaders, None)
	
    @staticmethod 
    def doPost(uri, oauthHeaders, body): 
        return LearningStudioUtility.__doMethod('POST', uri, oauthHeaders, body)
	
    @staticmethod 
    def doPut(uri, oauthHeaders, body):
        return LearningStudioUtility.__doMethod('PUT', uri, oauthHeaders, body)
	
    @staticmethod 
    def doDelete(uri, oauthHeaders):
        return LearningStudioUtility.__doMethod('DELETE', uri, oauthHeaders, None)

    @staticmethod
    def __doMethod(method, uri, oauthHeaders, body):
        is_xml = uri.lower().endswith('.xml')
        m = method.upper()
        byte_array = None
        has_content = (m == 'POST' or m == 'PUT')
        http_conn, parts = parse_url_and_connect (uri)
        log_debug('--------REQUEST URL--------')
        log_debug('%s %s' % (m, uri,))
        oauthHeaders['User-Agent'] = 'LS-HelloWorld'
        if has_content:
            if type(body) is str: byte_array = body.encode(encoding = 'UTF-8')
            else: byte_array = body.decode(encoding = 'UTF-8')
            oauthHeaders['Content-Type'] = 'application/xml' if is_xml else 'application/json'
            oauthHeaders['Content-Length'] = str(len(byte_array))
        log_debug('--------REQUEST HEADERS--------')
        log_debug(str(oauthHeaders))
        if has_content:
            log_debug('--------REQUEST CONTENT--------')
            log_debug(body)
        log_debug('Parts PATH: ' + parts.path)
        http_conn.request(m, parts.path, byte_array, oauthHeaders)
        r = http_conn.getresponse()
        response_code = r.status
        log_debug('--------RESPONSE HEADERS--------')
        log_debug(r.getheaders())
        if response_code != 200 and response_code != 201:
            log_debug('--------RESPONSE CONTENT--------')
            log_debug(r.read())
            return Response(status_code = response_code, 
                            reason = r.reason,
                            content_type = 'text/plain',
                            content = str (response_code))
		
        content_type = 'application/json'
        for hdr in r.getheaders():
            if hdr[0].lower() == 'content-type':
                content_type = hdr[1]
                break
        content = r.read()			
        log_debug('--------RESPONSE CONTENT--------')
        log_debug(content)
        return Response(status_code = response_code, 
                        reason = r.reason,
                        content_type = content_type,
                        content = content)
