"""This file holds the Parent class which is used by the tmdbcall modules."""
import requests
import requests_cache
import logging
from celery import shared_task
from celery.contrib.methods import task_method

# The cache of requests is set to a sqlite Database named test_cache.
# The cache is deleted after one hour (3600 Seconds).
requests_cache.install_cache('test_cache', backend='sqlite', expire_after=3600)

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

_handler = logging.FileHandler('tmdbcall.log')
_handler.setLevel(logging.DEBUG)

_formatter = logging.Formatter('%(asctime)s - %(name)s -'
                               '%(levelname)s - %(message)s')
_handler.setFormatter(_formatter)
_logger.addHandler(_handler)


class _Parent(object):
    """
    The Parent class is a master class for all tmdbcall classes.

    It defines the base_uri, headers and params and base functions.

    Attributes:
        base_uri (str): Base URI to the TMDB API
        headers (dict): Base Headers, accept only json
        params (dict): Base params, the API_KEY
    """

    def __init__(self):
        """Import the API_KEY. Set the base_uri, headers and params."""
        from ._key import _API_KEY
        self.base_uri = 'https://api.themoviedb.org/3/'
        self.params = {'api_key': _API_KEY}
        self.headers = {'Accept': 'application/json'}

    # TODO Make Task work
    @shared_task(bind=True, filter=task_method, rate_limit='4/s')
    def make_request(self, target, json=True, headers=0, params=0):
        """Make a request to the given target.

        Either uses the given headers and params or the default ones.

        Args:
            target (str): Target URL for the request
            json (bool, optional): If set to false, the request is returned and
                not the parsed json.
            headers (dict, optional): Headers for request.
                If none is given the default is used
            params (dict, optional): Parametes for request.
                If none is given the default is used
        """
        if params is 0:
            params = self.params
        if headers is 0:
            headers = self.headers
        try:
            request = requests.get(
                target, headers=headers, params=params)
            request.raise_for_status()
            if json:
                return request.json()
            else:
                return request
        except (
            requests.exceptions.RequestException, ValueError,
                requests.exceptions.HTTPError,
                requests.exceptions.Timeout) as e:
            _logger.warning(e)
            return False
