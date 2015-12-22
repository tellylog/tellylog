"""This file holds the tests for the Job class."""
from django.test import TestCase

from tmdbcall.job import Job


class TestJob(TestCase):
    """
    Testcases for the Job class

    Attributes:
        test (Job): Test instance of the Job class
    """
    test = Job()

    def test_get_jobs(self):
        """
        Test if the get_jobs() method returns a dictionary with the jobs key.
        """
        result = self.test.get_jobs()
        if 'jobs' in result:  # Check if the jobs key exists in the dict
            got_jobs = True
        else:
            got_jobs = False
        self.assertTrue(got_jobs)
