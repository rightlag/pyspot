# pyspot

pyspot 0.0.1

Released: 19-Jul-2015

---

# Introduction

pyspot is a Python package that provides an interface to the [Spotify RESTful web API](https://developer.spotify.com/web-api/).

Currently, this SDK does **not** provide methods to access all endpoints of the Spotify web API. I will continue to add functionality for the rest of the endpoints in due time.

I encourage other developers to create issues and submit pull requests if there exists errors or improvements can be made to the SDK.

# Getting started with pyspot

Your credentials can be passed when instantiating the Spotify class. Alternatively, pyspot will check for the existence of the following environment variables:

**SPOTIFY_CLIENT_ID** - Your Spotify client ID

**SPOTIFY_CLIENT_SECRET** - Your Spotify client secret

Credentials can also be stored in a pyspot configuration file.
