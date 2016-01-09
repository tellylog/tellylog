"""This module holds the Genre class."""
from ._parent import _Parent


class Genre(_Parent):

    """
    Class to get Genre Data.

    Attributes:
        URLS (dict): All relevant urls
    """

    URLS = {
        'genre_list': 'genre/tv/list',
    }

    def get_genres(self):
        """Get a list of all tv genres.

        Builds the URL to the target and makes a request.
        """
        target = self.base_uri + self.URLS['genre_list']
        response = self.make_request.apply(kwargs={
            'target': target, 'params': self.params, 'headers': self.headers})

        return response
