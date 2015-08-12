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
