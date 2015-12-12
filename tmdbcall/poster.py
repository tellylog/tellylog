"""
This file holds the Poster class which is used to get
poster Imgages from the TheMovieDataBase API.
"""
from io import BytesIO
from PIL import Image
from .parent import Parent


class Poster(Parent):
    poster_size = "w185/"

    def __init__(self):
        super().__init__()
        self.base_uri = 'https://image.tmdb.org/t/p/'
        self.headers = {}

    def get_poster(self, imagename):
        target = self.base_uri + self.poster_size + imagename
        result = self.make_request(target=target, json=False)
        try:
            poster = Image.open(BytesIO(result.content))
            return poster  # TODO: Make return Image from Pillow
        except AttributeError:
            return False
