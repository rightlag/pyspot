import exception
import httplib
import json
import urllib

from base64 import b64encode


class Token(object):
    Host = 'accounts.spotify.com'

    def __init__(self, client_id=None, client_secret=None):
        """
        The `Token` class uses the Client Credentials Flow model
        described here:

            https://developer.spotify.com/web-api/authorization-guide/#client_credentials_flow

        This flow does not include authorization and therefore cannot be
        used to access or manage a user's private data.
        """
        conn = httplib.HTTPSConnection(self.Host)
        body = {
            'grant_type': 'client_credentials',
        }
        body = urllib.urlencode(body)
        auth = b64encode('{}:{}'.format(client_id, client_secret))
        headers = {
            'Authorization': 'Basic ' + auth,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        conn.request('POST', '/api/token', body=body, headers=headers)
        res = conn.getresponse()
        if res.status != 200:
            raise exception.SpotifyServerError(res.status, res.reason)
        res = json.loads(res.read())
        self.access_token = res['access_token']
        self.token_type = res['token_type']
        self.expires_in = res['expires_in']
