import models


class Factory(object):
    """A factory to determine the class to instantiate via the `type`
    attribute from the response returned from the API.
    """
    @staticmethod
    def build(type):
        # Return appropriate class via HTTP response content. The `Category`
        # and `PlaylistTrack` models do not contain the `type` attribute. If
        # the `type` is `None`, then the factory returns the `Category` and
        # `PlaylistTrack` classes. The `items` attribute then iterates though
        # both classes and tries to instantiate the correct class based on the
        # response returned from the request.
        if type is None:
            return (models.Category, models.PlaylistTrack,)
        else:
            return {
                'album': (models.AlbumSimplified, models.AlbumFull),
                'artist': (models.ArtistSimplified, models.ArtistFull),
                'playlist': (models.PlaylistSimplified, models.PlaylistFull),
                'track': (models.TrackSimplified, models.TrackFull),
            }[type]
