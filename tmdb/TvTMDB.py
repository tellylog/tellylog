"""
This file holds the TvTMDB class which is used to get
TV-Data from the TheMovieDataBase API.
"""
import requests
import requests_cache

from django.conf import settings

# The cache of requests is set to a sqlite Database named test_cache.
# The cache is deleted after one hour (3600 Seconds).
requests_cache.install_cache('test_cache', backend='sqlite', expire_after=3600)


class TvTMDB(object):

    """
    Class to get TV-Data from the TheMovieDataBase.
    The JSON responses are converted to Objects.
    If an Error occurs the class raises an exception.

    Attributes:
        API_KEY (str): API Key stored in the settings
        BASE_URL (str): Base URL to TheMovieDataBase
        GENRE_LIST (str): Url to the Genre List
        HEADERS (dict): Default Headers for the request
        JOB_LIST (str): Url to the Job List
        PARAMS (dict): Default parameters for the request
        SEARCH_SERIES (str): Url to the TV Search
        TIMEOUT (int): Seconds after which Timeout is raised
    """
    BASE_URL = "http://api.themoviedb.org/3/"
    API_KEY = settings.TMDB_API_KEY
    TIMEOUT = 1
    PARAMS = {'api_key': API_KEY}
    HEADERS = {'Accept': 'application/json'}
    GENRE_LIST = BASE_URL + "genre/tv/list"
    JOB_LIST = BASE_URL + "job/list"
    SEARCH_SERIES = BASE_URL + "search/tv"  # needs a second get parameter
    TV_URL = BASE_URL + "tv/"
    SERIES_URL = TV_URL + "{id}"  # id is replaced by series_id
    SEASON_URL = TV_URL + "{id}/season/{number}"

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
            params = self.PARAMS
        if headers is 0:
            headers = self.HEADERS
        try:
            request = requests.get(
                target, headers=headers, params=params, timeout=self.TIMEOUT)
            request.raise_for_status()
            return request.json()
        except (
            requests.exceptions.RequestException, ValueError,
                requests.exceptions.HTTPError,
                requests.exceptions.Timeout) as e:
            # TODO Logging of Exceptions
            return False

    def get_genres(self):
        """Get a list of all tv genres.
        Builds the URL to the target and makes a request.
        """
        response = self.make_request(target=self.GENRE_LIST)
        return response

    def get_jobs(self):
        """Get a list of all valid Jobs

        Returns:
            dict: A dictionary of all Jobs
            bool: False if an error occurred
        """
        response = self.make_request(target=self.JOB_LIST)
        return response

    def search_for_series(self, query, page=None):
        """Tries to find the series on the basis of the query parameter.

        Args:
            query (str): The search string
            page (int, optional): The page that should be loaded

        Returns:
            dict: A dictionary of the series search results
            bool: False if an error occurred
        """
        if page is None:
            page = 1
        params = self.PARAMS
        params['query'] = query  # Append the Query to the default params
        params['page'] = page
        response = self.make_request(target=self.SEARCH_SERIES, params=params)
        if not response:
            return False
        if response['total_results'] is 0:
            return False
        else:
            return response

    def get_series_info_by_id(self, series_id):
        """Get detailed Information of a Series by the tmdb ID

        Args:
            id (int): TheMovieDataBase Series ID

        Returns:
            bool: False on error
            dict: A dictionary with the series data
        """
        target = self.SERIES_URL.format(id=series_id)
        response = self.make_request(target=target)
        if not response:
            return False
        return response

    def get_season_info_by_number(self, series_id, season_number):
        """Get information of a Season by the tmdb ID.
        Result includes episodes

        Args:
            series_id (int): TheMovieDataBase Series ID
            season_number (int): Description

        Returns:
            bool: False on error
            dict: A dictionary with the season data
        """
        target = self.SEASON_URL.format(id=series_id, number=season_number)
        response = self.make_request(target=target)
        if not response:
            return False
        return response
