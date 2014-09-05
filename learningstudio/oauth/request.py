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
request
-------

Objects representing OAuth requests.


"""

class OAuthRequest(object):
    """Represents a basic OAuth request object.

    """

    def __init__(self, headers):
        self.__headers = headers

    def __str__(self):
        s = ''
        for key, value in self.__headers.iteritems():
            s += '%s=%s\n' % (key, value)
        return s

    def __repr__(self): return self.__str__()

    def getHeaders(self): 
        """Returns the OAuth headers.

        :returns: The OAuth headers.
        :rtype: dict

        """
        return self.__headers

class OAuth1Request(OAuthRequest):
    """Represents an OAuth1 request object.

    """

    def __init__(self, headers, signature):
        self.__signature = signature
        super(OAuth1Request, self).__init__(headers)

    def __str__(self):
        s = super(OAuth1Request, self).__str__()
        s += '\n'
        s += self.__signature
        return s

    def __repr__(self): return self.__str__()

    def getSignature(self): 
        """Returns the OAuth1 signature.

        :returns: The signature string.
        :rtype: str

        """
        return self.__signature

class OAuth2Request(OAuthRequest):
    """Represents an OAuth2 request object.

    """

    def __init__(self, headers, 
                 access_token, refresh_token,
                 expires_in_seconds, creation_time):
        super(OAuth2Request, self).__init__(headers)
        self.__access_token = access_token
        self.__refresh_token = refresh_token
        self.__expires_in_seconds = expires_in_seconds
        self.__creation_time = creation_time
        self.__expiration_time = 0
        if self.__creation_time != None and self.__expires_in_seconds != None:
            self.__expiration_time = self.__creation_time + (self.__expires_in_seconds * 1000)

    def getAccessToken(self): 
        """Returns the access token.

        :returns: The access token.
        :rtype: str

        """
        return self.__access_token

    def getRefreshToken(self): 
        """Returns the refresh token.

        :returns: The refresh token.
        :rtype: str

        """
        return self.__refresh_token

    def getExpiresInSeconds(self): 
        """Returns the time in which this authtoken will expire.

        :returns: Time to expire in seconds.
        :rtype: long

        """
        return self.__expires_in_seconds

    def getCreationTime(self): 
        """Returns the time at which this object was created.

        :returns: The creation time object
        :rtype: time

        """
        return self.__creation_time

    def getExpirationTime(self): 
        """Returns the time in which this authtoken will expire.

        :returns: The expiration time object
        :rtype: time
        
        """
        return self.__expiration_time

