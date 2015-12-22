"""This file is used to get the API_KEY."""
import os
from getenv import env

try:
    if os.environ['CI'] is not None:
        _API_KEY = os.environ['TMDB_API_KEY']
except:
    _API_KEY = env('TMDB_API_KEY')
