import hashlib
from io import BytesIO
import PIL
from tmdbcall.tv import TV
from tmdbcall.poster import Poster
from tv import models
from django.core.files.base import ContentFile


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
    tmdb_poster = Poster()
    poster_large = tmdb_poster.get_poster(poster_path=poster_path)
    if poster_large:
        size = (180, 270)
        poster_small = poster_large.resize(size, PIL.Image.ANTIALIAS)
    else:
        poster_large = None
        poster_small = None
    return {'poster_large': (hashlib.md5(poster_large.tobytes()).hexdigest(),
                             poster_large),
            'poster_small': (hashlib.md5(poster_small.tobytes()).hexdigest(),
                             poster_small)}


def _check_countrys(countrys):
    country_list = []
    for country in countrys:
        db_country = models.Country.objects.get_or_create(name=country,
                                                          defaults={
                                                              'name': country
                                                          })
        if type(db_country) is tuple:
            country_list.append(db_country[0])
        else:
            country_list.append(db_country)
    return country_list


def convert_series_result(result):
    tmdb_tv = TV()
    full_series = tmdb_tv.get_series_info_by_id(result['id'])
    genre_list = _check_genres(full_series['genres'])
    country_list = _check_countrys(full_series['origin_country'])
    runtime = _calc_av_episode_runtime(full_series['episode_run_time'])
    posters = _get_posters(poster_path=full_series['poster_path'])
    new_series = models.Series(name=full_series['name'],
                               tmdb_id=full_series['id'],
                               in_production=full_series['in_production'],
                               first_air_date=full_series['first_air_date'],
                               last_air_date=full_series['last_air_date'],
                               episode_run_time=runtime,
                               number_of_episodes=full_series[
                                   'number_of_episodes'],
                               number_of_seasons=full_series[
                                   'number_of_seasons'],
                               original_language=full_series[
                                   'original_language'],
                               overview=full_series['overview'],
                               status=full_series['status'],
                               type=full_series['type'])
    temp_poster = BytesIO()
    posters['poster_large'][1].save(temp_poster, 'JPEG')
    temp_poster.seek(0)
    new_series.poster_large.save(posters['poster_large'][0] + '.jpg',
                                 ContentFile(temp_poster.read()),
                                 save=False)
    temp_poster.close()
    temp_poster = BytesIO()
    posters['poster_small'][1].save(temp_poster, 'JPEG')
    temp_poster.seek(0)
    new_series.poster_small.save(posters['poster_small'][0] + '.jpg',
                                 ContentFile(temp_poster.read()),
                                 save=False)
    temp_poster.close()
    new_series.save()
    new_series.genres.set(genre_list)
    new_series.origin_country.set(country_list)
