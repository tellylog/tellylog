"""
This module holds all tests for the TvTMDB class
"""
from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import TestCase

from tmdbcall.tv import TV

VALID_SERIES_NAME = "Malcolm in the Middle"
VALID_SERIES_ID = 2004
VALID_SEASON_NUMBER = 1
INVALID_SERIES_NAME = "m31573r h4ck3r"
INVALID_SERIES_ID = 0
INVALID_SEASON_NUMBER = 200


class TestTV(TestCase):

    """
    Testcases for the TV class

    Attributes:
        test (TV): Test instance of the TV class
    """
    test = TV()

    def test_search_for_series_with_valid_series(self):
        """Test if a dictionary is returned on a valid search query"""
        result = self.test.search_for_series(query=VALID_SERIES_NAME)
        self.assertEqual(result['results'][0]['name'], VALID_SERIES_NAME)

    def test_search_for_series_with_invalid_series(self):
        """
        Test if False is returned on an invalid search query.
        """
        result = self.test.search_for_series(query=INVALID_SERIES_NAME)
        self.assertFalse(result)

    def test_get_series_info_by_id_with_valid_id(self):
        """
        The function should return a dictionary on success.
        """
        result = self.test.get_series_info_by_id(series_id=VALID_SERIES_ID)
        self.assertEqual(result['id'], VALID_SERIES_ID)

    @patch('tmdbcall.parent.logger')  # Mocks the logger
    def test_get_series_info_by_id_with_invalid_id(self, mock_logging):
        """
        The function should return False on fail.
        And log the error to tmdbcall.log
        """
        result = self.test.get_series_info_by_id(series_id=INVALID_SERIES_ID)
        self.assertFalse(result)
        self.assertTrue(mock_logging.warning.called)  # Check if warning logged

    def test_get_season_info_by_number_with_valid_number(self):
        """
        The function should return a dictionary on success.
        """
        result = self.test.get_season_info_by_number(
            series_id=VALID_SERIES_ID, season_number=VALID_SEASON_NUMBER)
        self.assertEqual(result['season_number'], VALID_SEASON_NUMBER)

    @patch('tmdbcall.parent.logger')  # Mocks the logger
    def test_get_season_info_by_number_with_invalid_number(self, mock_logging):
        """
        The function should return false on fail.
        And log the error to tmdbcall.log
        """
        result = self.test.get_season_info_by_number(
            series_id=VALID_SERIES_ID, season_number=INVALID_SEASON_NUMBER)
        self.assertFalse(result)
        self.assertTrue(mock_logging.warning.called)  # Check if warning logged

    def test_get_changes_with_valid_id_and_date(self):
        """
        Should return a dict or False.
        """
        start_date = datetime.today() - timedelta(days=3)
        start_date = start_date.strftime('%Y-%m-%d')
        result = self.test.get_changes(VALID_SERIES_ID, start_date=start_date)
        try:
            self.assertIsInstance(result, dict)
        except self.failureException:
            self.assertFalse(result)

    def test_get_changes_with_invalid_id_and_valid_date(self):
        """
        Should return a dict or False.
        """
        start_date = datetime.today() - timedelta(days=3)
        start_date = start_date.strftime('%Y-%m-%d')
        result = self.test.get_changes(INVALID_SERIES_ID,
                                       start_date=start_date)
        try:
            self.assertIsInstance(result, dict)
        except self.failureException:
            self.assertFalse(result)

    def test_get_changes_with_invalid_id_and_invalid_date(self):
        """
        Should return False.
        """
        start_date = datetime.today() - timedelta(weeks=20)
        start_date = start_date.strftime('%Y-%m-%d')
        result = self.test.get_changes(INVALID_SERIES_ID,
                                       start_date=start_date)
        self.assertFalse(result)

    def test_get_changes_with_valid_id_and_invalid_date_in_past(self):
        """
        Should return a dict or False.
        """
        start_date = datetime.today() - timedelta(weeks=20)
        start_date = start_date.strftime('%Y-%m-%d')
        result = self.test.get_changes(VALID_SERIES_ID,
                                       start_date=start_date)
        try:
            self.assertIsInstance(result, dict)
        except self.failureException:
            self.assertFalse(result)

    def test_get_changes_with_valid_id_and_invalid_date_in_future(self):
        """
        Should return a dict or False.
        """
        start_date = datetime.today() + timedelta(weeks=3)
        start_date = start_date.strftime('%Y-%m-%d')
        result = self.test.get_changes(VALID_SERIES_ID,
                                       start_date=start_date)
        try:
            self.assertIsInstance(result, dict)
        except self.failureException:
            self.assertFalse(result)
