"""
This module gets data from TheMovieDataBase
"""
import os

from getenv import env

from .tv import TV
from .genre import Genre
from .job import Job

try:
    if os.environ['CI'] is not None:
        API_KEY = os.environ['TMDB_API_KEY']
except:
    API_KEY = env('TMDB_API_KEY')
