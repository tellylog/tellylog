"""This file holds the Parent class which is used by the tmdbcall modules."""
from io import BytesIO
from PIL import Image
import requests
import requests_cache
from celery import shared_task
from celery.contrib.methods import task_method
from ._logging import logger

# The cache of requests is set to a redis Database named test_cache.
# The cache is deleted after one hour (3600 Seconds).
requests_cache.install_cache('tmdb_cache', backend='redis', expire_after=3600)


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

    # make_request is a celery task. it has a rate_limit
    @shared_task(filter=task_method, rate_limit='4/s')
    def make_request(target, headers, params, json=True):
        """Make a request to the given target.
        Either uses the given headers and params or the default ones.
        Args:
            target (str): Target URL for the request
            json (bool): If set to false, the request is returned and
                not the parsed json.
            headers (dict): Headers for request.
                If none is given the default is used
            params (dict): Parametes for request.
                If none is given the default is used
        """
        try:
            print('Making a request master')
            request = requests.get(
                target, headers=headers, params=params)
            request.raise_for_status()
            if json:
                print('It is from the json type master')
                return request.json()
            else:
                print('It is from the image type master')
                temp = Image.open(BytesIO(request.content))
                poster = {
                    'data': temp.tobytes(),
                    'size': temp.size,
                    'mode': temp.mode,
                }
                return poster
        except (
            requests.exceptions.RequestException, ValueError,
                requests.exceptions.HTTPError,
                requests.exceptions.Timeout) as e:
            logger.warning(e)
            return False
