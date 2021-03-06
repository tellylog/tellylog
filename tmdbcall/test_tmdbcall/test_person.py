"""
This file holds the tests for the Person class

Attributes:
    INVALID_PERSON_ID (int): A nonexistant person id
    VALID_PERSON_ID (int): An existing valid person id
"""
import time
import unittest

from datetime import datetime, timedelta

from django.test import TestCase
from tmdbcall.person import Person

VALID_PERSON_ID = 71580  # Benedict Cumberbatch
INVALID_PERSON_ID = 0


@unittest.skip("Needs new implementation.")
class TestPerson(TestCase):
    """
    Class for the test functions

    Attributes:
        test (Person): The test instance of Person
    """
    test = Person()

    def test_get_person_with_valid_id(self):
        """
        A valid ID should return a dict.
        """
        result = self.test.get_person(VALID_PERSON_ID)
        while result.status in result.UNREADY_STATES:
            time.sleep(0.1)
        self.assertEqual(result.result['id'], VALID_PERSON_ID)

    def test_get_person_with_invalid_id(self):
        """
        The function should return false on fail
        """
        result = self.test.get_person(INVALID_PERSON_ID)
        while result.status in result.UNREADY_STATES:
            time.sleep(0.1)
        self.assertFalse(result.result)

    def test_get_changes_with_valid_id_and_date(self):
        """
        Should return a dict or False.
        """
        start_date = datetime.today() - timedelta(days=3)
        start_date = start_date.strftime('%Y-%m-%d')
        result = self.test.get_changes(VALID_PERSON_ID, start_date=start_date)
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
        result = self.test.get_changes(INVALID_PERSON_ID,
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
        result = self.test.get_changes(INVALID_PERSON_ID,
                                       start_date=start_date)
        self.assertFalse(result)

    def test_get_changes_with_valid_id_and_invalid_date_in_past(self):
        """
        Should return a dict or False.
        """
        start_date = datetime.today() - timedelta(weeks=20)
        start_date = start_date.strftime('%Y-%m-%d')
        result = self.test.get_changes(VALID_PERSON_ID,
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
        result = self.test.get_changes(VALID_PERSON_ID,
                                       start_date=start_date)
        try:
            self.assertIsInstance(result, dict)
        except self.failureException:
            self.assertFalse(result)
