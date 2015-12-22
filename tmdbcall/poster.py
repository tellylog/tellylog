"""This file holds the Poster class which is used to get poster Imgages."""
from io import BytesIO
from PIL import Image
from .parent import _Parent


class Poster(_Parent):
    """
    The Poster Class can get Images from TheMovieDataBase.

    It uses the Pillow (PIL) module for the Image class.

    Attributes:
        base_uri (str): Base URI to the Images
        headers (dict): Base Headers for requests
        poster_size (str): Base Size for the Images
    """

    poster_size = "w185/"

    def __init__(self):
        """
        Overwrite the default base_uri and the headers of the Parent class.

        base_uri points now to the image base uri
        headers are now empty
        """
        super().__init__()
        self.base_uri = 'https://image.tmdb.org/t/p/'
        self.headers = {}

    def get_poster(self, imagename):
        """
        Get the Poster via the Name of the Image.

        Args:
            imagename (str): Valid Imagename (e.g.
                                              44FcYhsLNjJA6d2ce5rYfaIVAJU.jpg)

        Returns:
            bool: False if it fails
            Image: If valid image is returned
        """
        target = self.base_uri + self.poster_size + imagename
        result = self.make_request(target=target, json=False)
        try:
            poster = Image.open(BytesIO(result.content))
            return poster
        except AttributeError:
            return False
