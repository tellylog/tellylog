"""
This file holds the Image class which is used to get
Imgages from the TheMovieDataBase API.
"""
from .parent import Parent
# import Pillow needs to be here


class Image(Parent):
    poster_size = "w185/"

    def __init__(self):
        super().__init__()
        self.base_uri = 'https://image.tmdb.org/t/p/'
        self.headers = {}

    def get_poster(self, imagename):
        target = self.base_uri + self.poster_size + imagename
        result = self.make_request(target=target, json=False)
        return result  # TODO: Make return Image from Pillow
