import helpers
import httplib
import json

from urlparse import urlparse


class Paging(httplib.HTTPSConnection, object):
    def __init__(self,
                 href,
                 items,
                 limit,
                 next,
                 offset,
                 previous,
                 total):
        """The offset-based paging object is a container for a set of
        objects.

        https://developer.spotify.com/web-api/object-model/#paging-object
        """
        # Assign fqdn as host.
        host = urlparse(href).netloc
        super(Paging, self).__init__(host)
        type = items[0].get('type')
        # Return appropriate class via HTTP response content. The
        # `Category` and `PlaylistTrack` models do not contain the
        # `type` attribute. If the `type` is `None`, then the factory
        # returns the `Category` and `PlaylistTrack` classes. The
        # `items` attribute then iterates though both classes and tries
        # to instantiate the correct class based on the response
        # returned from the request.
        try:
            klass = helpers.Factory.build(type)
            self.items = [klass(**item) for item in items]
        except TypeError:
            for kls in klass:
                try:
                    self.items = [kls(**item) for item in items]
                except TypeError:
                    continue
        self.limit = limit
        self.next = next
        self.offset = offset
        self.previous = previous
        self.total = total

    def next(self):
        if self.next:
            url = urlparse(self.next)
            url = url.path + '?' + url.query
            self.request('GET', url)
            res = self.getresponse()
            res = json.loads(res.read())
            # Reinitialize the `Paging` object with updated attributes
            # returned from HTTP response.
            return self.__init__(**res)
        else:
            raise StopIteration

    def __str__(self):
        return '{}:{}'.format(self.__class__.__name__, self.total)

    def __repr__(self):
        return '{}:{}'.format(self.__class__.__name__, self.total)


class AlbumSimplified(object):
    def __init__(self,
                 album_type=None,
                 available_markets=[],
                 external_urls={},
                 href=None,
                 id=None,
                 images=[],
                 name=None,
                 type=None,
                 uri=None):
        self.album_type = album_type
        self.available_markets = available_markets
        self.external_urls = ExternalURL(external_urls)
        self.href = href
        self.id = id
        self.images = [Image(**image) for image in images]
        self.name = name
        self.type = type
        self.uri = uri

    def __unicode__(self):
        return u'{}:{}'.format(self.__class__.__name__, self.name)

    def __repr__(self):
        return unicode(self).encode('utf8')


class AlbumFull(AlbumSimplified):
    def __init__(self,
                 album_type=None,
                 artists=[],
                 available_markets=[],
                 copyrights=[],
                 external_ids={},
                 external_urls={},
                 genres=[],
                 href=None,
                 id=None,
                 images=[],
                 name=None,
                 popularity=None,
                 release_date=None,
                 release_date_precision=None,
                 tracks=[],
                 type=None,
                 uri=None):
        super(AlbumFull, self).__init__(album_type,
                                        available_markets,
                                        external_urls,
                                        href,
                                        id,
                                        images,
                                        name,
                                        type,
                                        uri)
        self.artists = [ArtistSimplified(**artist) for artist in artists]
        self.copyrights = [Copyright(**copyright) for copyright in copyrights]
        self.external_ids = ExternalID(external_ids)
        self.genres = genres
        self.popularity = popularity
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.tracks = Paging(**tracks)


class ArtistSimplified(object):
    def __init__(self,
                 external_urls={},
                 href=None,
                 id=None,
                 name=None,
                 type=None,
                 uri=None):
        self.external_urls = ExternalURL(external_urls)
        self.href = href
        self.id = id
        self.name = name
        self.type = type
        self.uri = uri

    def __unicode__(self):
        return u'{}:{}'.format(self.__class__.__name__, self.name)

    def __repr__(self):
        return unicode(self).encode('utf8')


class ArtistFull(ArtistSimplified):
    def __init__(self,
                 external_urls={},
                 followers=None,
                 genres=[],
                 href=None,
                 id=None,
                 images=[],
                 name=None,
                 popularity=None,
                 type=None,
                 uri=None):
        super(ArtistFull, self).__init__(external_urls,
                                         href,
                                         id,
                                         name,
                                         type,
                                         uri)
        self.followers = Followers(**followers)
        self.genres = genres
        self.images = [Image(**image) for image in images]
        self.popularity = popularity


class Category(object):
    def __init__(self,
                 href=None,
                 icons=[],
                 id=None,
                 name=None):
        self.href = href
        self.icons = [Image(**icon) for icon in icons]
        self.id = id
        self.name = name

    def __str__(self):
        return '{}:{}'.format(self.__class__.__name__, self.name)

    def __repr__(self):
        return '{}:{}'.format(self.__class__.__name__, self.name)


class Copyright(object):
    def __init__(self,
                 text=None,
                 type=None):
        self.text = text
        self.type = type

    def __str__(self):
        return '{}:{}'.format(self.__class__.__name__, self.text)

    def __repr__(self):
        return '{}:{}'.format(self.__class__.__name__, self.text)


class ExternalID(dict):
    pass


class ExternalURL(dict):
    pass


class Followers(object):
    def __init__(self,
                 href=None,
                 total=None):
        self.href = href
        self.total = total

    def __str__(self):
        return '{}:{}'.format(self.__class__.__name__, self.total)

    def __repr__(self):
        return '{}:{}'.format(self.__class__.__name__, self.total)


class Image(object):
    def __init__(self,
                 height=None,
                 url=None,
                 width=None):
        self.height = height
        self.url = url
        self.width = width

    def __str__(self):
        return '{}:{}'.format(self.__class__.__name__, self.url)

    def __repr__(self):
        return '{}:{}'.format(self.__class__.__name__, self.url)


class PlaylistSimplified(object):
    def __init__(self,
                 collaborative=None,
                 external_urls={},
                 href=None,
                 id=None,
                 images=[],
                 name=None,
                 owner=None,
                 public=None,
                 snapshot_id=None,
                 tracks=None,
                 type=None,
                 uri=None):
        self.collaborative = collaborative
        self.external_urls = ExternalURL(external_urls)
        self.href = href
        self.id = id
        self.images = [Image(**image) for image in images]
        self.name = name
        self.owner = UserPublic(**owner)
        self.public = public
        self.snapshot_id = snapshot_id
        self.tracks = tracks
        self.type = type
        self.uri = uri

    def __unicode__(self):
        return u'{}:{}'.format(self.__class__.__name__, self.name)

    def __repr__(self):
        return unicode(self).encode('utf8')


class PlaylistFull(PlaylistSimplified):
    def __init__(self,
                 collaborative=None,
                 description=None,
                 external_urls={},
                 followers=None,
                 href=None,
                 id=None,
                 images=[],
                 name=None,
                 owner=None,
                 public=None,
                 snapshot_id=None,
                 tracks=None,
                 type=None,
                 uri=None):
        super(PlaylistFull, self).__init__(collaborative,
                                           external_urls,
                                           href,
                                           id,
                                           images,
                                           name,
                                           owner,
                                           public,
                                           snapshot_id,
                                           tracks,
                                           type,
                                           uri)
        self.description = description
        self.followers = Followers(**followers)


class PlaylistTrack(object):
    def __init__(self,
                 added_at=None,
                 added_by=None,
                 is_local=None,
                 track=None):
        self.added_at = added_at
        self.added_by = UserPublic(**added_by)
        self.is_local = is_local
        self.track = TrackFull(**track)

    def __unicode__(self):
        return u'{}:{}'.format(self.__class__.__name__, self.track.name)

    def __repr__(self):
        return unicode(self).encode('utf8')


class TrackSimplified(object):
    def __init__(self,
                 artists=[],
                 available_markets=[],
                 disc_number=None,
                 duration_ms=None,
                 explicit=None,
                 external_urls={},
                 href=None,
                 id=None,
                 is_playable=None,
                 linked_from=None,
                 name=None,
                 preview_url=None,
                 track_number=None,
                 type=None,
                 uri=None):
        self.artists = [ArtistSimplified(**artist) for artist in artists]
        self.available_markets = available_markets
        self.disc_number = disc_number
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.external_urls = ExternalURL(external_urls)
        self.href = href
        self.id = id
        self.is_playable = is_playable
        self.linked_from = linked_from
        self.name = name
        self.preview_url = preview_url
        self.track_number = track_number
        self.type = type
        self.uri = uri

        if not available_markets:
            # For track relinking purposes.
            # See: https://developer.spotify.com/web-api/track-relinking-guide/
            del self.available_markets

    def __unicode__(self):
        return u'{}:{}'.format(self.__class__.__name__, self.name)

    def __repr__(self):
        return unicode(self).encode('utf8')


class TrackFull(TrackSimplified):
    def __init__(self,
                 album=None,
                 artists=[],
                 available_markets=[],
                 disc_number=None,
                 duration_ms=None,
                 explicit=None,
                 external_ids={},
                 external_urls={},
                 href=None,
                 id=None,
                 is_playable=None,
                 linked_from=None,
                 name=None,
                 popularity=None,
                 preview_url=None,
                 track_number=None,
                 type=None,
                 uri=None):
        super(TrackFull, self).__init__(artists,
                                        available_markets,
                                        disc_number,
                                        duration_ms,
                                        explicit,
                                        external_urls,
                                        href,
                                        id,
                                        is_playable,
                                        linked_from,
                                        name,
                                        preview_url,
                                        track_number,
                                        type,
                                        uri)
        self.album = AlbumSimplified(**album)
        self.external_ids = ExternalID(external_ids)
        self.popularity = popularity


class TrackLink(object):
    def __init__(self,
                 external_urls={},
                 href=None,
                 id=None,
                 type=None,
                 uri=None):
        self.external_urls = ExternalURL(external_urls)
        self.href = href
        self.id = id
        self.type = type
        self.uri = uri

    def __str__(self):
        return '{}:{}'.format(self.__class__.__name__, self.type)

    def __repr__(self):
        return '{}:{}'.format(self.__class__.__name__, self.type)


class UserPublic(object):
    def __init__(self,
                 display_name=None,
                 external_urls={},
                 followers=None,
                 href=None,
                 id=None,
                 images=[],
                 type=None,
                 uri=None):
        self.display_name = display_name
        self.external_urls = ExternalURL(external_urls)
        self.followers = Followers(followers)
        self.href = href
        self.id = id
        self.images = [Image(**image) for image in images]
        self.type = type
        self.uri = uri

    def __unicode__(self):
        return u'{}:{}'.format(self.__class__.__name__, self.id)

    def __repr__(self):
        return unicode(self).encode('utf8')


class UserPrivate(UserPublic):
    def __init__(self,
                 birthdate=None,
                 country=None,
                 display_name=None,
                 email=None,
                 external_urls={},
                 followers=None,
                 href=None,
                 id=None,
                 images=[],
                 product=None,
                 type=None,
                 uri=None):
        super(UserPrivate, self).__init__(display_name,
                                          external_urls,
                                          followers,
                                          href,
                                          id,
                                          images,
                                          type,
                                          uri)
        self.birthdate = birthdate
        self.country = country
        self.email = email
        self.product = product
