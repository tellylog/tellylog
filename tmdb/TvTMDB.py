import requests

from django.conf import settings


class TvTMDB(object):
    """
    Class to make calls for TV Information to The Movie Database
    JSON responses are converted to Objects
    """
    BASE_URL = "http://api.themoviedb.org/3/"
    API_KEY = settings.TMDB_API_KEY
    PARAMS = {'api_key': API_KEY}
    GENRE_LIST = "genre/tv/list"
    JOB_LIST = "job/list"

    def sendRequest(self, target):
        request = requests.get(target, params=self.PARAMS)
        return request

    def getGenres(self):
        target = self.BASE_URL + self.GENRE_LIST
        print(self.sendRequest(target=target))
