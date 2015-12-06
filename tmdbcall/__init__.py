"""
This module gets data from TheMovieDataBase
"""
from getenv import env

from .tv import TV
from .genre import Genre
from .job import Job

try:
    API_KEY = env('TMDB_API_KEY')
except ImproperlyConfigured:
    raise
