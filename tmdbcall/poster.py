"""This file holds the Poster class which is used to get poster Imgages."""
import os
from io import BytesIO
from PIL import Image

from ._parent import _Parent


class Poster(_Parent):

    """
    The Poster Class can get Images from TheMovieDataBase.

    It uses the Pillow (PIL) module for the Image class.

    Attributes:
        base_uri (str): Base URI to the Images
        headers (dict): Base Headers for requests
        poster_size (str): Base Size for the Images
    """

    poster_size = "w342/"

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
        # Make the request with json set to False
        request = self.make_request.delay(
            target=target, headers=self.headers,
            params=self.params, json=False)
        response = request.get()
        if 'data' in response:
            try:
                # create a PIL Image from the Bytes
                poster = Image.frombytes(
                    mode=response['mode'],
                    size=response['size'],
                    data=response['data']
                    )
                return poster
            except (AttributeError, TypeError):
                # return False if something goes wrong
                return False
        else:
            # no response -> False
            return False
