import json
import os


class Config(object):
    def __init__(self):
        attrs = {}
        try:
            # Load client ID and client secret from environment variables.
            attrs['CLIENT_ID'] = os.environ['SPOTIFY_CLIENT_ID']
            attrs['CLIENT_SECRET'] = os.environ['SPOTIFY_CLIENT_SECRET']
        except KeyError:
            # Load client ID and client secret from configuration file.
            filepath = os.path.join(os.path.expanduser('~'), '.pyspot')
            with open(filepath, 'rb') as f:
                try:
                    params = json.loads(f.read())
                except TypeError, e:
                    raise e
                attrs['CLIENT_ID'] = params['SPOTIFY_CLIENT_ID']
                attrs['CLIENT_SECRET'] = params['SPOTIFY_CLIENT_SECRET']
        self.attrs = attrs

    def get(self, key):
        try:
            return self.attrs[key]
        except KeyError:
            return None
