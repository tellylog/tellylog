import os
from getenv import env

try:
    if os.environ['CI'] is not None:
        API_KEY = os.environ['TMDB_API_KEY']
except:
    API_KEY = env('TMDB_API_KEY')
