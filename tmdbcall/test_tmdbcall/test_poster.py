"""
This module holds all tests for the Poste class

Attributes:
    INVALID_IMAGE_NAME (str): Invalid image name
    VALID_IMAGE_NAME (str): Valid image name (Elementary Poster)
"""
from unittest.mock import patch
from django.test import TestCase
from tmdbcall import Poster


VALID_IMAGE_NAME = '44FcYhsLNjJA6d2ce5rYfaIVAJU.jpg'
INVALID_IMAGE_NAME = 'gimme_the_pic.jpg'


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
        self.assertIsInstance(result.info, dict)
        self.assertEqual(result.format, 'JPEG')

    @patch('tmdbcall.parent._logger')  # Mocks the logger
    def test_get_poster_with_invalid_name(self, mock_logging):
        """
        Should return False and the incident should get logged.
        """
        result = self.test.get_poster(INVALID_IMAGE_NAME)
        self.assertFalse(result)
        self.assertTrue(mock_logging.warning.called)  # Check if warning logged