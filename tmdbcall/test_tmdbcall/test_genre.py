"""This file holds the tests for the Genre class."""
from django.test import TestCase

from tmdbcall.genre import Genre


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
        if result:
            # Check if the genres key exists in the dict
            if 'genres' in result:
                got_genres = True
            else:
                got_genres = False
        else:
            got_genres = False
        self.assertTrue(got_genres)
