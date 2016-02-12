"""This file holds the tests for the Job class."""
import time
import unittest

from django.test import TestCase
from tmdbcall.job import Job


@unittest.skip("Needs new implementation.")
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
        while result.status in result.UNREADY_STATES:
            time.sleep(0.1)
        if result.result:
            # Check if the jobs key exists in the dict
            if 'jobs' in result.result:
                got_jobs = True
            else:
                got_jobs = False
        else:
            got_jobs = False
        self.assertTrue(got_jobs)
