# -*- coding: utf-8 -*-
import unittest

from pyspot import models
from pyspot import Spotify


class SpotifyTestCase(unittest.TestCase):
    def setUp(self):
        self.spotify = Spotify()

    def test_http_basic_authentication_token_is_set(self):
        self.assertIsNotNone(getattr(self.spotify, 'token'))

    def test_if_available_markets_attribute_exists(self):
        # For track relinking
        # https://developer.spotify.com/web-api/track-relinking-guide/
        # "Heaven and Hell" - William Onyeabor
        track = self.spotify.get_track(
            id='6kLCHFM39wkFjOuyPGLGeQ',
            market='US'
        )
        self.assertFalse(hasattr(track, 'available_markets'))
        self.assertIsNotNone(track.is_playable)

    def test_playlist_full_tracks_attribute_is_instance_of_paging(self):
        # Assert that the `tracks` attribute of the `PlaylistFull` object is
        # an instance of the `Paging` class.
        playlist = self.spotify.get_playlist(
            user_id='spotify',
            playlist_id='59ZbFPES4DQwEjBpWHzrtC',
        )
        self.assertTrue(isinstance(playlist.tracks, models.Paging))

    def test_pagination_with_paging_object(self):
        # Assert that paging object supports iteration.
        tracks = self.spotify.get_albums_tracks(
            id='6akEvsycLGftJxYudPjmqK',
            limit=5
        )
        self.assertEqual(tracks.limit, 5)
        if tracks.next:
            next(tracks)
            self.assertIsNotNone(tracks.items)

    def test_get_album_endpoint(self):
        album = self.spotify.get_album(id='5OpMncQPaqLOvFkwAiTKSY')
        self.assertTrue(isinstance(album, models.AlbumFull))
        self.assertEqual(album.name, 'Pink')
        self.assertTrue(isinstance(album.tracks, models.Paging))
        self.assertTrue(hasattr(album, 'available_markets'))

    def test_get_album_endpoint_with_params(self):
        album = self.spotify.get_album(id='5OpMncQPaqLOvFkwAiTKSY',
                                       market='AD')
        self.assertFalse(hasattr(album, 'available_markets'))
        for track in album.tracks.items:
            self.assertTrue(hasattr(track, 'is_playable'))

    def test_get_several_albums_endpoint(self):
        albums = self.spotify.get_several_albums(ids=[
            '41MnTivkwTO3UUJ8DrqEJJ',
            '6JWc4iAiJ9FjyK0B59ABb4',
            '6UXCm6bOO4gFlDQZV5yL37',
        ])
        self.assertEqual(albums[0].name, 'The Best Of Keane (Deluxe Edition)')
        self.assertEqual(albums[1].name, 'Strangeland')
        self.assertEqual(albums[2].name, 'Night Train')

    def test_get_albums_tracks_endpoint(self):
        tracks = self.spotify.get_albums_tracks(
            id='6akEvsycLGftJxYudPjmqK',
            limit=2
        )
        self.assertEqual(tracks.limit, 2)

    def test_get_artist_endpoint(self):
        artist = self.spotify.get_artist(id='0OdUWJ0sBjDrqHygGUXeCF')
        self.assertTrue(isinstance(artist, models.ArtistFull))

    def test_get_artists_albums_endpoint_with_params(self):
        artist_albums = self.spotify.get_artists_albums(
            id='1vCWHaC5f2uS3yhpwWbIA6',
            album_type='single',
            limit=2
        )
        self.assertEqual(artist_albums.limit, 2)
        for album in artist_albums.items:
            self.assertEqual(album.album_type, 'single')

    def test_get_list_featured_playlists_endpoint_with_params(self):
        featured_playlists = self.spotify.get_list_featured_playlists(
            country='US',
            timestamp='2014-10-23T07:00:00'
        )
        self.assertTrue(
            isinstance(featured_playlists['playlists'], models.Paging)
        )

    def test_get_list_categories_endpoint(self):
        categories = self.spotify.get_list_categories()
        for category in categories.items:
            self.assertTrue(isinstance(category, models.Category))

    def test_get_categorys_playlists_endpoint_with_params(self):
        categorys_playlists = self.spotify.get_categorys_playlists(
            category_id='party',
            country='BR',
            limit=2
        )
        for playlist in categorys_playlists.items:
            self.assertTrue(isinstance(playlist, models.PlaylistSimplified))

    def test_search_item_endpoint_with_params(self):
        # Searching for artists
        artists = self.spotify.search_item(type='artist', q='tania bowra')
        for artist in artists.items:
            self.assertTrue(isinstance(artist, models.ArtistFull))
        # Searching for artists, using a wildcard
        artists = self.spotify.search_item(type='artist', q='tania*')
        for artist in artists.items:
            self.assertTrue(isinstance(artist, models.ArtistFull))
        # Searching for artists with name matching "Bob", and offset, and limit
        artists = self.spotify.search_item(
            type='artist',
            q='bob',
            offset=20,
            limit=2
        )
        self.assertEqual(artists.offset, 20)
        self.assertEqual(artists.limit, 2)
        for artist in artists.items:
            self.assertTrue(isinstance(artist, models.ArtistFull))
        # Searching for albums with name matching "Arrival" and artist
        # matching "ABBA"
        albums = self.spotify.search_item(
            type='album',
            q='album:arrival artist:abba'
        )
        for album in albums.items:
            self.assertTrue(isinstance(album, models.AlbumSimplified))
        # Searching for album with specific UPC code
        albums = self.spotify.search_item(type='album', q='upc:5099908217059')
        for album in albums.items:
            self.assertTrue(isinstance(album, models.AlbumSimplified))
        # Searching for playlists with name or description matching a string
        playlists = self.spotify.search_item(type='playlist', q='doom metal')
        for playlist in playlists.items:
            self.assertTrue(isinstance(playlist, models.PlaylistSimplified))
        # Searching only for tracks available in a specific market
        tracks = self.spotify.search_item(type='track', q='abba', market='US')
        for track in tracks.items:
            self.assertTrue(isinstance(track, models.TrackFull))

    def test_get_users_profile_endpoint(self):
        user = self.spotify.get_users_profile(user_id='tuggareutangranser')
        self.assertTrue(isinstance(user, models.UserPublic))
        self.assertTrue(isinstance(user.followers, models.Followers))

    def test_get_list_users_playlists_endpoint(self):
        users_playlists = self.spotify.get_list_users_playlists(
            user_id='wizzler'
        )
        for playlist in users_playlists.items:
            self.assertTrue(isinstance(playlist, models.PlaylistSimplified))

    def test_get_playlist_endpoint_with_params(self):
        playlist = self.spotify.get_playlist(
            user_id='spotify',
            playlist_id='59ZbFPES4DQwEjBpWHzrtC'
        )
        self.assertTrue(isinstance(playlist, models.PlaylistFull))
        for track in playlist.tracks.items:
            self.assertTrue(isinstance(track, models.PlaylistTrack))
