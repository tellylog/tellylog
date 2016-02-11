"""This file holds the tests for the Genre class."""
import time
import unittest

from django.test import TestCase
from tmdbcall.genre import Genre


@unittest.skip("Needs new implementation.")
class TestGenre(TestCase):

    """
    Testcases for the Genre class

    Attributes:
        test (Genre): Test instance of the Genre class
    """
    test = Genre()

    def test_get_genres(self):
        """
        Test if the get_genres() method returns a
        dictionary with the genres key.
        """
        result = self.test.get_genres()
        while result.status in result.UNREADY_STATES:
            time.sleep(0.1)
        if result.result:
            # Check if the genres key exists in the dict
            if 'genres' in result.result:
                got_genres = True
            else:
                got_genres = False
        else:
            got_genres = False
        self.assertTrue(got_genres)
