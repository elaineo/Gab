__author__ = "Elaine Ou, elaineo"
__date__ = "December 18, 2018"
__license__ = "MIT"

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from .constants import *
import base64
import requests


OAUTH_SUBDOMAIN = 'api'
OAUTH_ENDPOINT = 'oauth/token'


class Auth(requests.auth.AuthBase):

    """Request bearer access token for oAuth2 authentication.
    :param consumer_key: Twitter application consumer key
    :param consumer_secret: Twitter application consumer secret
    :param proxies: Dictionary of proxy URLs (see documentation for python-requests).
    """

    def __init__(self, client_id, client_secret, access_token=None):
        self._client_id = client_id
        self._client_secret = client_secret
        if not access_token:
            self._access_token = self._get_access_token()
        else:
            self._access_token = access_token

    def _get_access_token(self):
        token_url = '%s://%s.%s/%s' % (PROTOCOL,
                                       OAUTH_SUBDOMAIN,
                                       DOMAIN,
                                       OAUTH_ENDPOINT)
        try:
            client = BackendApplicationClient(client_id=client_id)
            oauth = OAuth2Session(client=client)
            token = oauth.fetch_token(
                token_url=token_url, 
                client_id=self._client_id, 
                client_secret=self._client_secret)
            return token
        except Exception as e:
            raise Exception('Error requesting bearer access token: %s' % e)

    def __call__(self, r):
        auth_list = [
            self._client_id,
            self._client_secret,
            self._access_token]
        if all(auth_list):
            r.headers['Authorization'] = "Bearer %s" % self._access_token
            return r
        else:
            raise Exception('Not enough keys passed to Bearer token manager.')