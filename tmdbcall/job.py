"""This module holds the Job class"""
from .parent import _Parent


class Job(_Parent):
    """
    Class to get Job Data.

    Attributes:
        URLS (dict): Holds all relevant URLS
    """
    URLS = {
        'job_list': 'job/list',
    }

    def get_jobs(self):
        """Get a list of all valid Jobs

        Returns:
            dict: A dictionary of all Jobs
            bool: False if an error occurred
        """
        target = self.base_uri + self.URLS['job_list']
        response = self.make_request(target=target)
        return response
