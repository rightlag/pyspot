# pyspot

pyspot 0.0.1

Released: 19-Jul-2015

---

# Introduction

pyspot is a Python package that provides an interface to the [Spotify RESTful web API](https://developer.spotify.com/web-api/).

I encourage other developers to create issues and submit pull requests if there exists errors or improvements can be made to the SDK.

# Getting started with pyspot

Your credentials can be passed when instantiating the Spotify class. Alternatively, pyspot will check for the existence of the following environment variables:

**SPOTIFY_CLIENT_ID** - Your Spotify client ID

**SPOTIFY_CLIENT_SECRET** - Your Spotify client secret

Credentials can also be stored in a pyspot configuration file.

```json
{
    "SPOTIFY_CLIENT_ID": "<YOUR_SPOTIFY_CLIENT_ID>",
    "SPOTIFY_CLIENT_SECRET": "<YOUR_SPOTIFY_CLIENT_SECRET>"
}
```

# Sample endpoint request

```python
from pyspot import Spotify
from pyspot.exception import SpotifyServerError


# use credentials from ~/.pyspot configuration file
spotify = Spotify()
try:
    track = spotify.get_track(id='6kLCHFM39wkFjOuyPGLGeQ', market='US')
except SpotifyServerError, e:
    raise e
print track.name, '-', track.artists[0].name # Heaven and Hell - William Onyeabor
```

# Iterating through `Paging` objects

The Spotify Web API contains a [Paging](https://developer.spotify.com/web-api/object-model/#paging-object) object that serves as a container for a set of objects.

To `Paging` object supports iteration by calling the `next` method. An example below shows how to paginate through a list of `Track` objects wrapped in a `Paging` object:

```python
from pyspot import Spotify
from pyspot.exception import SpotifyServerError

spotify = Spotify()
try:
    tracks = spotify.get_albums_tracks(
        id='6akEvsycLGftJxYudPjmqK',
        limit=1
    )
except pyspot.exception.SpotifyServerError, e:
    raise e
# Print the first element of the track
print tracks.items
while tracks.next:
    # If the `next` attribute is not None, continue to iterate through the
    # `Track` objects.
    next(tracks)
    print tracks.items
```
