"""This module holds the Job class."""
from ._parent import _Parent


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
        """Get a list of all valid Jobs.

        Returns:
            dict: A dictionary of all Jobs
            bool: False if an error occurred
        """
        target = self.base_uri + self.URLS['job_list']
        request = self.make_request.delay(
            target=target, headers=self.headers, params=self.params, json=True)
        try:
            response = request.get()
        except:
            response = False
        return response
