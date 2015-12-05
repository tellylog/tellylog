"""This file holds all tests for the TvTMDB class"""
from django.test import TestCase

from .tmdb.TvTMDB import TvTMDB


class TvTMDBTests(TestCase):
    """This class holds the test cases for the TvTMDB class"""

    def test_make_request_to_404(self):
        """Check if the status code to a 404 page is correct."""
        tvtmdb = TvTMDB()
        target = "http://httpbin.org/status/404"
        headers = None
        params = None
        response = tvtmdb.make_request(
            target=target, headers=headers, params=params)
        self.assertEqual(response.status_code, 404)
