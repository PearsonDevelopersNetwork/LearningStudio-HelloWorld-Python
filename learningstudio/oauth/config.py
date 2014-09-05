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
config
------

Configuration objects for initializing OAuth1 and OAuth2 services.


"""

def oauth_config(application_id, application_name = '',
                 client_string = '', consumer_key = '', 
                 consumer_secret = ''):
    """Creates a new OAuth configuration.

    :param application_id: The unique identifier of the client application.
    :type application_id: str
    :param application_name: Name of the client application.
    :type application_name: str
    :param client_string: The unique client string.
    :type client_string: str
    :param consumer_key: The key required to receive a request token.
    :type consumer_key: str
    :param consumer_secret: The secret required to receive a request token.
    :type consumer_secret: str

    :returns: The new oauth configuration.
    :rtype: dict

    """
    return { 'application_id' : application_id,
             'application_name' : application_name,
             'client_string' : client_string,
             'consumer_key' : consumer_key,
             'consumer_secret' : consumer_secret }

def oauth1_signature_config(application_id, consumer_key,
                            consumer_secret):
    """Convenience function for creating an OAuth1 signature configuration.

    :param application_id: The unique identifier of the client application.
    :type application_id: str
    :param consumer_key: The key required to receive a request token.
    :type consumer_key: str
    :param consumer_secret: The secret required to receive a request token.
    :type consumer_secret: str

    :returns: The new oauth configuration.
    :rtype: dict

    """
    return oauth_config(application_id, consumer_key = consumer_key,
                        consumer_secret = consumer_secret)

def oauth2_assertion_config(application_id, application_name,
                            client_string, consumer_key,
                            consumer_secret):
    """Convenience function for creating an OAuth2 assertion configuration.
    
    :param application_id: The unique identifier of the client application.
    :type application_id: str
    :param application_name: Name of the client application.
    :type application_name: str
    :param client_string: The unique client string.
    :type client_string: str
    :param consumer_key: The key required to receive a request token.
    :type consumer_key: str
    :param consumer_secret: The secret required to receive a request token.
    :type consumer_secret: str

    :returns: The new oauth configuration.
    :rtype: dict

    """
    return oauth_config(application_id, application_name,
                        client_string, consumer_key,
                        consumer_secret)

def oauth2_password_config(application_id, client_string):
    """Convenience function for creating an OAuth2 password configuration.
    
    :param application_id: The unique identifier of the client application.
    :type application_id: str
    :param client_string: The unique client string.
    :type client_string: str

    :returns: The new oauth configuration.
    :rtype: dict

    """
    return oauth_config(application_id, client_string = client_string)

def application_id(config):
    """Returns the application_id from the configuration.

    :param config: Configuration to extract the application_id from.
    :type config: dict

    :returns: The application_id from the configuration.
    :rtype: str

    """
    return config['application_id']

def application_name(config):
    """Returns the application_name from the configuration.

    :param config: Configuration to extract the application_name from.
    :type config: dict

    :returns: The application_name from the configuration.
    :rtype: str

    """

    return config['application_name']

def client_string(config):
    """Returns the client_string from the configuration.

    :param config: Configuration to extract the client_string from.
    :type config: dict

    :returns: The client_string from the configuration.
    :rtype: str

    """

    return config['client_string']

def consumer_secret(config):
    """Returns the consumer_secret from the configuration.

    :param config: Configuration to extract the consumer_secret from.
    :type config: dict

    :returns: The consumer_secret from the configuration.
    :rtype: str

    """

    return config['consumer_secret']

def consumer_key(config):
    """Returns the consumer_key from the configuration.

    :param config: Configuration to extract the consumer_key from.
    :type config: dict

    :returns: The consumer_key from the configuration.
    :rtype: str

    """

    return config['consumer_key']
