import requests
import requests_cache

# The cache of requests is set to a sqlite Database named test_cache.
# The cache is deleted after one hour (3600 Seconds).
requests_cache.install_cache('test_cache', backend='sqlite', expire_after=3600)


class Parent(object):
    """docstring for Parent"""
    def __init__(self):
        from . import API_KEY
        self.base_uri = 'https://api.themoviedb.org/3/'
        self.params = {'api_key': API_KEY}
        self.headers = {'Accept': 'application/json'}

    def make_request(self, target, headers=0, params=0):
        """Make a request to the given target.
        Either uses the given headers and params or the default ones.

        Args:
            target (str): Target URL for the request
            headers (dict, optional): Headers for request.
                If none is given the default is used
            params (TYPE, optional): Parametes for request.
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
            return request.json()
        except (
            requests.exceptions.RequestException, ValueError,
                requests.exceptions.HTTPError,
                requests.exceptions.Timeout) as e:
            # TODO Logging of Exceptions
            return False

    def convert_dict(self, response={}):
        if isinstance(response, dict):
            for key in response.keys():
                setattr(self, key, response[key])
