class SpotifyClientError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message


class SpotifyServerError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message

    def __str__(self):
        return '%d %s' % (self.status, self.message)

    def __repr__(self):
        return '%d %s' % (self.status, self.message)


class SpotifyConfigurationException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
