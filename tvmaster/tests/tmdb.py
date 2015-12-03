from urllib2 import Request, urlopen

from django.conf import settings


class TvTMDB(object):
    """
    Class to make calls for TV Information to The Movie Database
    JSON responses are converted to Objects
    """
    BASE_URL = "http://api.themoviedb.org/3/"
    API_KEY = settings.TMDP_API_KEY
    POSTFIX = "?api_key=" + API_KEY
    GENRE_LIST = "genre/tv/list"
    JOB_LIST = "job/list"

    HEADERS = {
        'Accept': 'application/json'
    }

    def sendRequest(target):
        pass

    def getGenres():
        pass
