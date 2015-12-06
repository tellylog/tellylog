"""
This module gets data from TheMovieDataBase
"""

from django.conf import settings

from .tv import TV
from .genre import Genre
from .job import Job

API_KEY = settings.TMDB_API_KEY
