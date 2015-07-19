import unittest

from src.pyspot import Spotify


class SpotifyTestCase(unittest.TestCase):
    def setUp(self):
        self.spotify = Spotify()

    def test_http_basic_authentication_token_has_been_set(self):
        self.assertIsNotNone(getattr(self.spotify, 'token'))

    def test_if_available_markets_attribute_exists(self):
        # "Heaven and Hell" - William Onyeabor
        track = self.spotify.get_track(id='6kLCHFM39wkFjOuyPGLGeQ',
                                       market='US')
        self.assertFalse(hasattr(track, 'available_markets'))
        self.assertIsNotNone(track.is_playable)

if __name__ == '__main__':
    unittest.main()
