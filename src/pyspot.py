import exception
import httplib
import json
import models
import urllib

from auth import Token
from config import Config


class Spotify(object):
    Host = 'api.spotify.com'
    Version = 'v1'
    BaseUri = '/{version}'.format(version=Version)
    ResponseError = exception.SpotifyServerError

    def __init__(self, client_id=None, client_secret=None):
        if client_id and client_secret:
            self.token = Token(client_id=client_id,
                               client_secret=client_secret)
        else:
            config = Config()
            self.token = Token(
                client_id=config.attrs['CLIENT_ID'],
                client_secret=config.attrs['CLIENT_SECRET']
            )
        # Set the bearer for each HTTP request regardless if OAuth is
        # required or not.
        self.headers = {
            'Authorization': '{token.token_type} {token.access_token}'.format(
                token=self.token
            ),
            'Content-Type': 'application/json',
        }

    def get_album(self, id=None, **kwargs):
        url = self.BaseUri + '/albums/{id}'.format(id=id)
        res = self._request('GET', url, **kwargs)
        return models.AlbumFull(**res)

    def get_several_albums(self, ids=None, **kwargs):
        url = self.BaseUri + '/albums?ids={ids}'.format(ids=ids)
        res = self._request('GET', url, **kwargs)
        return [models.AlbumFull(**album) for album in res['albums']]

    def get_albums_tracks(self, id=None, **kwargs):
        url = self.BaseUri + '/albums/{id}/tracks'.format(id=id)
        res = self._request('GET', url, **kwargs)
        return models.Paging(**res)

    def get_artist(self, id=None):
        url = self.BaseUri + '/artists/{id}'.format(id=id)
        res = self._request('GET', url)
        return models.ArtistFull(**res)

    def get_several_artists(self, ids=None):
        url = self.BaseUri + '/artists?ids={ids}'.format(ids=ids)
        res = self._request('GET', url)
        return [models.ArtistFull(**artist) for artist in res['artists']]

    def get_artists_albums(self, id=None, **kwargs):
        url = self.BaseUri + '/artists/{id}/albums'.format(id=id)
        res = self._request('GET', url, **kwargs)
        return models.Paging(**res)

    def get_artists_top_tracks(self, id=None, **kwargs):
        url = self.BaseUri + '/artists/{id}/top-tracks'.format(id=id)
        res = self._request('GET', url, **kwargs)
        return [models.TrackFull(**track) for track in res['tracks']]

    def get_related_artists(self, id=None):
        url = self.BaseUri + '/artists/{id}/related-artists'.format(id=id)
        res = self._request('GET', url)
        return [models.ArtistFull(**artist) for artist in res['artists']]

    def get_list_featured_playlists(self, **kwargs):
        url = self.BaseUri + '/browse/featured-playlists'
        res = self._request('GET', url, **kwargs)
        return {
            'message': res.get('message'),
            'playlists': models.Paging(**res['playlists']),
        }

    def get_list_new_releases(self, **kwargs):
        url = self.BaseUri + '/browse/new-releases'
        res = self._request('GET', url, **kwargs)
        return {
            'message': res.get('message'),
            'albums': models.Paging(**res['albums']),
        }

    def get_list_categories(self, **kwargs):
        url = self.BaseUri + '/browse/categories'
        res = self._request('GET', url, **kwargs)
        return models.Paging(**res['categories'])

    def get_track(self, id=None, **kwargs):
        url = self.BaseUri + '/tracks/{id}'.format(id=id)
        res = self._request('GET', url, **kwargs)
        return models.TrackFull(**res)

    def get_new_releases(self, **kwargs):
        url = self.BaseUri + '/browse/new-releases'
        res = self._request('GET', url, **kwargs)
        return models.Paging(**res['albums'])

    def _request(self, method, url, body=None, **kwargs):
        conn = httplib.HTTPSConnection(self.Host)
        if kwargs:
            # Additional query parameters. If the url already contains a
            # `?` character, then use an `&` character for additional
            # query parameters.
            url += '?' if '?' not in url else '&'
            url += urllib.urlencode(kwargs)
        conn.request(method, url, body=body, headers=self.headers)
        res = conn.getresponse()
        if res.status != 200:
            # Error in request, raise `SpotifyServerException`.
            raise self.ResponseError(res.status, res.reason)
        res = json.loads(res.read())
        return res

    def __str__(self):
        return '{}:{}'.format(
            self.__class__.__name__,
            self.token.access_token
        )

    def __repr__(self):
        return '{}:{}'.format(
            self.__class__.__name__,
            self.token.access_token
        )
