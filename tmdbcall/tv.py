"""
This file holds the TV class which is used to get
TV-Data from the TheMovieDataBase API.
"""
from .parent import Parent


class TV(Parent):

    """
    Class to get TV-Data from the TheMovieDataBase.
    The JSON responses are converted to Objects.
    If an Error occurs the class raises an exception.

    Attributes:
        URLS (dict): Holds all relevant URLS
    """

    URLS = {
        'search_series': 'search/tv',
        'tv_url': 'tv/',
        'series': '{id}',
        'season': '{id}/season/{number}'
    }

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
        params = self.params
        params['query'] = query  # Append the Query to the default params
        params['page'] = page
        target = self.base_uri + self.URLS['search_series']
        response = self.make_request(target=target, params=params)
        if not response:
            return False
        if response['total_results'] is 0:
            return False
        else:
            return response

    def get_series_info_by_id(self, series_id):
        """Get detailed Information of a Series by the tmdb ID

        Args:
            series_id (int): Description

        Returns:
            bool: False on error
            dict: A dictionary with the series data

        Deleted Parameters:
            id (int): TheMovieDataBase Series ID
        """
        target = self.base_uri + \
            self.URLS['tv_url'] + self.URLS['series'].format(id=series_id)
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
        target = self.base_uri + self.URLS['tv_url'] + \
            self.URLS['season'].format(id=series_id, number=season_number)
        response = self.make_request(target=target)
        if not response:
            return False
        return response
