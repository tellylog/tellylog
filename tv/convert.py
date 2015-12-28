import PIL
import tmdbcall as tmdb
from tv import models


def _check_genres(genres):
    genre_list = []
    for genre in genres:
        db_genre = models.Genre.objects.get_or_create(tmdb_id=genre['id'],
                                                      defaults={
                                                       'tmdb_id': genre['id'],
                                                       'name': genre['name']}
                                                      )
        if type(db_genre) is tuple:
            genre_list.append(db_genre[0])
        else:
            genre_list.append(db_genre)
    return genre_list


def _calc_av_episode_runtime(runtimes):
    return sum(runtimes) // len(runtimes)

def _get_posters(poster_path):
    poster_path = poster_path[1:]
    tmdb_poster = tmdb.poster.Poster()
    poster_large = tmdb_poster.get_poster(poster_path=poster_path)
    if poster_large:
        size = (180, 270)
        poster_medium = poster_large.resize(size, PIL.Image.ANTIALIAS)
    else:
        poster_large = None
        poster_medium = None
    return {'poster_large': poster_large,
            'poster_medium': poster_medium}


def convert_series_result(result):
    tmdb_tv = tmdb.tv.TV()
    full_series = tmdb_tv.get_series_info_by_id(result['id'])
    genre_list = _check_genres(full_series['genres'])
    runtime = _calc_av_episode_runtime(full_series['episode_run_time'])
    posters = _get_posters(poster_path=full_series['poster_path'])


