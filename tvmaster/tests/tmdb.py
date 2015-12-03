from urllib2 import Request, urlopen

from django.conf import settings


class TMDB(object):
    """docstring for TMDB"""

    api_key = settings.TMDP_API_KEY

    def function():
        pass
