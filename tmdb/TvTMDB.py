"""
This file holds the TvTMDB class which is used to get
TV-Data from the TheMovieDataBase API.
"""
import requests
import json

from django.conf import settings


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

    def search_for_series(self, query):
        """Tries to find the series on the basis of the query parameter.

        Args:
            query (str): The search string

        Returns:
            dict: A dictionary of all Jobs
            bool: False if an error occurred
        """
        page = 1
        params = self.PARAMS
        params['query'] = query  # Append the Query to the default params
        params['page'] = page
        response = {}
        response[1] = self.make_request(
            target=self.SEARCH_SERIES, params=params)
        if not response[1]:
            return False

        if response[1]['total_pages'] > 1:
            num_pages = response[1]['total_pages']
            if num_pages > 10:  # Protection against too many requests
                num_pages = 10
            # Add the number of the pages to the response for later use
            response['num_pages'] = num_pages
            for page in range(2, num_pages):  # Get all (max. 10) next pages
                params['page'] = page
                response[page] = self.make_request(
                    self.SEARCH_SERIES, params=params)

        if response[1]['total_results'] is 0:
            return False
        else:
            return response
