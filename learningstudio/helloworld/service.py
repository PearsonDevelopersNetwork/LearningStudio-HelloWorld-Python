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

import bottle
from bottle import route, get, post, put, delete, request, response, static_file

from learningstudio.oauth.util import parse_url
from learningstudio.oauth.config import *
from learningstudio.oauth.service import AuthMethod, OAuthServiceFactory
from learningstudio.helloworld.resource import *
from learningstudio.helloworld.util import *

LS_API_URL = 'https://api.learningstudio.com/'

APP_ROOT = '/helloworld'
OAUTH2_ASSERTION_ROOT = APP_ROOT + '/oauth2'
OAUTH1_SIGNATURE_ROOT = APP_ROOT + '/oauth1'

def oauth2_assertion_root(): return OAUTH2_ASSERTION_ROOT
def oauth1_signature_root(): return OAUTH1_SIGNATURE_ROOT

@route(APP_ROOT)
def server_static():
    return static_file('index.htm', root='./learningstudio/helloworld')

@get(OAUTH2_ASSERTION_ROOT + '/:path#.+#')
def get_oauth2_assertion(path):
    servlet = OAuth2AssertionServlet()
    return mk_web_response(servlet.do_GET(path))

@get(OAUTH1_SIGNATURE_ROOT + '/:path#.+#')
def get_oauth2_assertion(path):
    servlet = OAuth1SignatureServlet()
    return mk_web_response(servlet.do_GET(path))

@post(OAUTH2_ASSERTION_ROOT + '/:path#.+#')
def post_oauth2_assertion(path):
    servlet = OAuth2AssertionServlet()
    return mk_web_response(servlet.do_POST(path, request.body.read()))

@post(OAUTH1_SIGNATURE_ROOT + '/:path#.+#')
def post_oauth2_assertion(path):
    servlet = OAuth1SignatureServlet()
    return mk_web_response(servlet.do_POST(path, request.body.read()))

@put(OAUTH2_ASSERTION_ROOT + '/:path#.+#')
def put_oauth2_assertion(path):
    servlet = OAuth2AssertionServlet()
    return mk_web_response(servlet.do_PUT(path, request.body.read()))

@put(OAUTH1_SIGNATURE_ROOT + '/:path#.+#')
def put_oauth2_assertion(path):
    servlet = OAuth1SignatureServlet()
    return mk_web_response(servlet.do_PUT(path, request.body.read()))

@delete(OAUTH2_ASSERTION_ROOT + '/:path#.+#')
def put_oauth2_assertion(path):
    servlet = OAuth2AssertionServlet()
    return mk_web_response(servlet.do_DELETE(path))

@delete(OAUTH1_SIGNATURE_ROOT + '/:path#.+#')
def put_oauth2_assertion(path):
    servlet = OAuth1SignatureServlet()
    return mk_web_response(servlet.do_DELETE(path))

def mk_web_response(resp):
    if resp == None: return None
    response.set_header('Content-Type', resp.contentType())
    response.status = str(resp.statusCode()) + ' ' + resp.reason()
    return resp.content()

def get_query_string():
    return request.query_string

def remove_path_prefix(path):
    return path[path.find('/', 1):]

class OAuthServlet:
    def do_GET(self, path):
        return self.__do_method('GET', path)

    def do_POST(self, path, body):
        return self.__do_method('POST', path, body = body)

    def do_PUT(self, path, body):
        return self.__do_method('PUT', path, body = body)

    def do_DELETE(self, path):
        return self.__do_method('DELETE', path)

    def getOAuthHeaders(self, url, method, body):
        return { }

    def __do_method(self, method, path, body = None):
        if body != None and not(type(body) is str):
            body = body.decode(encoding = 'UTF-8')
        print("%s, %s, %s" % (method, path, body,))
        response = None
        query_string = get_query_string()
        if query_string != None and len(query_string) > 0:
            path = path + '?' + query_string

        url = LS_API_URL + path
        oauth_headers = self.getOAuthHeaders(url, method, body)
        if method == 'GET':
            response = LearningStudioUtility.doGet(url, oauth_headers)
        elif method == 'POST':
            response = LearningStudioUtility.doPost(url, oauth_headers, body)
        elif method == 'PUT':
            response = LearningStudioUtility.doPut(url, oauth_headers, body)
        elif method == 'DELETE':
            response = LearningStudioUtility.doDelete(url, oauth_headers)
            
        if response == None:
            response = Response(status_code = 405)
        return response

def get_factory():
    config = oauth_config(application_id = APPID,
                          application_name = APPNAME,
                          client_string = CLIENT_STRING,
                          consumer_key = KEY,
                          consumer_secret = SECRET)
    return OAuthServiceFactory(config)

class OAuth2AssertionServlet(OAuthServlet):
    def getOAuthHeaders(self, url, method, body):
        service = get_factory().build(AuthMethod.oauth2_assertion_service())
        headers = service.generateRequest(username = USERNAME).getHeaders()
        headers['User-Agent'] = 'LS-HelloWorld'
        return headers

class OAuth1SignatureServlet(OAuthServlet):
    def getOAuthHeaders(self, url, method, body):
        service = get_factory().build(AuthMethod.oauth1_signature_service())
        headers = service.generateRequest(url = url, http_method = method, body = body).getHeaders()
        headers['User-Agent'] = 'LS-HelloWorld'
        return headers

def run():
    bottle.run()

if __name__ == "__main__":
    run()
