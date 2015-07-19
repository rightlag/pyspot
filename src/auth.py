import httplib
import json
import urllib

from base64 import b64encode


class Token(object):
    Host = 'accounts.spotify.com'

    def __init__(self, client_id=None, client_secret=None):
        """Return auth body via `client_id` and `client_secret`.

        base64 encode `client_id` and `client_secret` before making a
        HTTP POST request to the /api/token endpoint.
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
        res = json.loads(res.read())
        self.access_token = res['access_token']
        self.token_type = res['token_type']
        self.expires_in = res['expires_in']

    def __str__(self):
        return '{}:{}'.format(self.__class__.__name__, self.access_token)

    def __repr__(self):
        return '{}:{}'.format(self.__class__.__name__, self.access_token)
