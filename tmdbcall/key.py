"""This file is used to get the API_KEY."""
import os
from getenv import env

if os.getenv('CI') is not None:
    _API_KEY = os.environ['TMDB_API_KEY']
else:
    _API_KEY = env('TMDB_API_KEY')
