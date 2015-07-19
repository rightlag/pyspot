import models


class Factory(object):
    """A factory to determine the class to instantiate via the `type`
    attribute from the response returned from the API.
    """
    @staticmethod
    def build(type):
        return {
            'album': models.AlbumSimplified,
            'artist': models.ArtistSimplified,
            'playlist': models.PlaylistSimplified,
            'track': models.TrackSimplified,
        }[type]
