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
            self.token = Token(
                client_id=client_id,
                client_secret=client_secret
            )
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
        """Get Spotify catalog information for a single album."""
        url = '/albums/{id}'.format(id=id)
        res = self._request('GET', url, **kwargs)
        return models.AlbumFull(**res)

    def get_several_albums(self, ids=None, **kwargs):
        """Get Spotify catalog information for multiple albums
        identified by their Spotify IDs."""
        ids = ','.join([str(id) for id in ids])
        url = '/albums?ids={ids}'.format(ids=ids)
        res = self._request('GET', url, **kwargs)
        return [models.AlbumFull(**album) for album in res['albums']]

    def get_albums_tracks(self, id=None, **kwargs):
        """Get Spotify catalog information about an album's tracks.
        Optional parameters can be used to limit the number of tracks
        returned."""
        url = '/albums/{id}/tracks'.format(id=id)
        res = self._request('GET', url, **kwargs)
        return models.Paging(**res)

    def get_artist(self, id=None):
        """Get Spotify catalog information for a single artist
        identified by their unique Spotify ID."""
        url = '/artists/{id}'.format(id=id)
        res = self._request('GET', url)
        return models.ArtistFull(**res)

    def get_several_artists(self, ids=None):
        """Get Spotify catalog information for several artists based on
        their Spotify IDs."""
        url = '/artists?ids={ids}'.format(ids=ids)
        res = self._request('GET', url)
        return [models.ArtistFull(**artist) for artist in res['artists']]

    def get_artists_albums(self, id=None, **kwargs):
        """Get Spotify catalog information about an artist's albums.
        Optional parameters can be specified in the query string to
        filter and sort the response."""
        url = '/artists/{id}/albums'.format(id=id)
        res = self._request('GET', url, **kwargs)
        return models.Paging(**res)

    def get_artists_top_tracks(self, id=None, **kwargs):
        """Get Spotify catalog information about an artist's top tracks
        by country."""
        url = '/artists/{id}/top-tracks'.format(id=id)
        res = self._request('GET', url, **kwargs)
        return [models.TrackFull(**track) for track in res['tracks']]

    def get_related_artists(self, id=None):
        """Get Spotify catalog information about artists similar to a
        given artist. Similarity is based on analysis of the Spotify
        community's listening history."""
        url = '/artists/{id}/related-artists'.format(id=id)
        res = self._request('GET', url)
        return [models.ArtistFull(**artist) for artist in res['artists']]

    def get_list_featured_playlists(self, **kwargs):
        """Get a list of Spotify featured playlists (shown, for example,
        on a Spotify player's "Browse" tab)."""
        url = '/browse/featured-playlists'
        res = self._request('GET', url, **kwargs)
        return {
            'message': res.get('message'),
            'playlists': models.Paging(**res['playlists']),
        }

    def get_list_new_releases(self, **kwargs):
        """Get a list of new album releases featured in Spotify (shown,
        for example, on a Spotify player's "Browse" tab)."""
        url = '/browse/new-releases'
        res = self._request('GET', url, **kwargs)
        return {
            'message': res.get('message'),
            'albums': models.Paging(**res['albums']),
        }

    def get_list_categories(self, **kwargs):
        """Get a list of categories used to tag items in Spotify (on,
        for example, the Spotify player's "Browse" tab)."""
        url = '/browse/categories'
        res = self._request('GET', url, **kwargs)
        return models.Paging(**res['categories'])

    def get_category(self, id=None, **kwargs):
        """Get a single category used to tag items in Spotify (on, for
        example, the Spotify player's "Browse" tab)."""
        url = '/browse/categories/{id}'.format(id=id)
        res = self._request('GET', url, **kwargs)
        return models.Category(**res)

    def get_categorys_playlists(self, id=None, **kwargs):
        """Get a list of Spotify playlists tagged with a particular
        category."""
        url = '/browse/categories/{id}/playlists'.format(id=id)
        res = self._request('GET', url, **kwargs)
        return models.Paging(**res['playlists'])

    def search_item(self, type=None, **kwargs):
        """Get Spotify catalog information about artists, albums, tracks
        or playlists that match a keyword string."""
        url = '/search?type={type}'.format(type=type)
        res = self._request('GET', url, **kwargs)
        # The response object returns plural representations of the
        # object type (e.g. albums, artists, etc.)
        plural_type = '{type}s'.format(type=type)
        return models.Paging(**res[plural_type])

    def get_track(self, id=None, **kwargs):
        """Get Spotify catalog information for a single track identified
        by its unique Spotify ID."""
        url = '/tracks/{id}'.format(id=id)
        res = self._request('GET', url, **kwargs)
        return models.TrackFull(**res)

    def get_several_tracks(self, ids=None, **kwargs):
        """Get Spotify catalog information for multiple tracks based on
        their Spotify IDs."""
        ids = ','.join([str(id) for id in ids])
        url = '/tracks?ids={ids}'.format(ids=ids)
        res = self._request('GET', url, **kwargs)
        return [models.TrackFull(**track) for track in res['tracks']]

    def get_users_profile(self, user_id=None):
        """Get public profile information about a Spotify user."""
        url = '/users/{user_id}'.format(user_id=user_id)
        res = self._request('GET', url)
        return models.UserPublic(**res)

    def get_list_users_playlists(self, user_id=None, **kwargs):
        """Get a list of the playlists owned or followed by a Spotify
        user."""
        url = '/users/{user_id}/playlists'.format(user_id=user_id)
        res = self._request('GET', url, **kwargs)
        return models.Paging(headers=self.headers, **res)

    def get_playlist(self, user_id=None, playlist_id=None, **kwargs):
        """Get a playlist owned by a Spotify user."""
        url = '/users/{user_id}/playlists/{playlist_id}'.format(
            user_id=user_id,
            playlist_id=playlist_id
        )
        res = self._request('GET', url, **kwargs)
        return models.PlaylistFull(**res)

    def get_playlists_tracks(self, user_id=None, playlist_id=None, **kwargs):
        """Get full details of the tracks of a playlist owned by a
        Spotify user."""
        url = '/users/{user_id}/playlists/{playlist_id}/tracks'.format(
            user_id=user_id,
            playlist_id=playlist_id
        )
        res = self._request('GET', url, **kwargs)
        return models.Paging(headers=self.headers, **res)

    def _request(self, method, url, body=None, **kwargs):
        conn = httplib.HTTPSConnection(self.Host)
        url = self.BaseUri + url
        if kwargs:
            # Additional query parameters. If the url already contains a
            # `?` character, then use an `&` character for additional
            # query parameters.
            url += '?' if '?' not in url else '&'
            url += urllib.urlencode(kwargs)
        conn.request(method, url, body=body, headers=self.headers)
        res = conn.getresponse()
        # 2XX success status code.
        if not 200 <= res.status <= 299:
            # Error in request, raise `SpotifyServerException`.
            raise self.ResponseError(res.status, res.reason)
        res = json.loads(res.read())
        return res

    def __str__(self):
        return '{}'.format(self.__class__.__name__)

    def __repr__(self):
        return '{}'.format(self.__class__.__name__)
