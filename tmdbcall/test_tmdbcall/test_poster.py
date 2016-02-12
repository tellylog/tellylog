"""
This module holds all tests for the Poste class

Attributes:
    INVALID_IMAGE_NAME (str): Invalid image name
    VALID_IMAGE_NAME (str): Valid image name (Elementary Poster)
"""
import time
import unittest

from django.test import TestCase
from tmdbcall.poster import Poster


VALID_IMAGE_NAME = '44FcYhsLNjJA6d2ce5rYfaIVAJU.jpg'
INVALID_IMAGE_NAME = 'gimme_the_pic.jpg'


@unittest.skip("Needs new implementation.")
class TestPoster(TestCase):
    """
    This class holds the tests for the Poster class.

    Attributes:
        test (Poster): The Poster test instance
    """
    test = Poster()

    def test_get_poster_with_valid_name(self):
        """
        Should return a Image object.
        Image object shoul have info and format attributes.
        format should be a string with the value JPEG
        info should be a dict
        """
        result = self.test.get_poster(VALID_IMAGE_NAME)
        while result.status in result.UNREADY_STATES:
            time.sleep(0.1)
        if result.result:
            # Check if the data key exists in the dict
            if 'data' in result.result:
                got_poster = True
            else:
                got_poster = False
        else:
            got_poster = False
        self.assertTrue(got_poster)

    def test_get_poster_with_invalid_name(self):
        """
        Should return False.
        """
        result = self.test.get_poster(INVALID_IMAGE_NAME)
        while result.status in result.UNREADY_STATES:
            time.sleep(0.1)
        if result.result:
            # Check if the data key exists in the dict
            if 'data' in result.result:
                got_poster = True
            else:
                got_poster = False
        else:
            got_poster = False
        self.assertFalse(got_poster)
