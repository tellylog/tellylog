import requests
import requests_cache
import logging

# The cache of requests is set to a sqlite Database named test_cache.
# The cache is deleted after one hour (3600 Seconds).
requests_cache.install_cache('test_cache', backend='sqlite', expire_after=3600)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('tmdbcall.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s'
                              '- %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Parent(object):
    """docstring for Parent"""
    def __init__(self):
        from .key import API_KEY
        self.base_uri = 'https://api.themoviedb.org/3/'
        self.params = {'api_key': API_KEY}
        self.headers = {'Accept': 'application/json'}

    def make_request(self, target, json=True, headers=0, params=0):
        """Make a request to the given target.
        Either uses the given headers and params or the default ones.

        Args:
            target (str): Target URL for the request
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
            logger.warning(e)
            return False

    def convert_dict(self, response={}):
        if isinstance(response, dict):
            for key in response.keys():
                setattr(self, key, response[key])
