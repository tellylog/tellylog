import hashlib
import time
from io import BytesIO
import PIL
from tmdbcall.tv import TV
from tmdbcall.poster import Poster
from tv import models
from django.core.files.base import ContentFile
from celery import shared_task
from celery import states


@shared_task()
def _check_genres(full_series):
    genre_list = []
    if not full_series:
        return False
    if ('genres' in full_series and
            type(full_series['genres']) == list):
        for genre in full_series['genres']:
            db_genre = models.Genre.objects.get_or_create(
                tmdb_id=genre['id'], defaults={
                    'tmdb_id': genre['id'],
                    'name': genre['name']}
            )
            if type(db_genre) is tuple:
                genre_list.append(db_genre[0])
            else:
                genre_list.append(db_genre)

    full_series = {'series': full_series}
    full_series['genre_list'] = genre_list
    return full_series


@shared_task()
def _check_countrys(full_series):
    country_list = []
    if not full_series:
        return False
    if ('origin_country' in full_series['series'] and
            type(full_series['series']['origin_country']) == list):
        for country in full_series['series']['origin_country']:
            db_country = models.Country.objects.get_or_create(name=country,
                                                              defaults={
                                                               'name': country
                                                              })
            if type(db_country) is tuple:
                country_list.append(db_country[0])
            else:
                country_list.append(db_country)
    full_series['country_list'] = country_list
    return full_series


def _calc_av_episode_runtime(runtimes):
    if len(runtimes) > 0:
        return sum(runtimes) // len(runtimes)
    else:
        return None


def _get_posters(poster_path):
    if type(poster_path) is str:
        poster_path = poster_path[1:]
        tmdb_poster = Poster()
        poster_result = tmdb_poster.get_poster(imagename=poster_path)
        while poster_result.status in states.UNREADY_STATES:
            time.sleep(1)
        if poster_result.result and 'data' in poster_result.result:
            poster_result = poster_result.result
            poster_large = PIL.Image.frombytes(
                data=poster_result['data'],
                size=poster_result['size'],
                mode=poster_result['mode'])
            if poster_large:
                size = (180, 270)
                poster_small = poster_large.resize(size, PIL.Image.ANTIALIAS)
                return {'poster_large': (hashlib.md5(
                                         poster_large.tobytes()).hexdigest(),
                                         poster_large),
                        'poster_small': (hashlib.md5(
                                         poster_small.tobytes()).hexdigest(),
                                         poster_small)}
    return False


def _convert_season(tmdb_series_id, series_id, season_number, new_series):
    tmdb_tv = TV()
    full_season = tmdb_tv.get_season_info_by_number(tmdb_series_id,
                                                    season_number)
    while full_season.status in states.UNREADY_STATES:
        time.sleep(0.5)
    if full_season.status == states.SUCCESS:
        full_season = full_season.result
        if full_season:
            new_season = models.Season(number=full_season['season_number'],
                                       air_date=full_season['air_date'],
                                       name=full_season['name'],
                                       tmdb_id=full_season['id'],
                                       episode_count=len(
                                           full_season['episodes']),
                                       series=new_series
                                       )
            posters = _get_posters(poster_path=full_season['poster_path'])
            if posters:
                temp_poster = BytesIO()
                posters['poster_large'][1].save(temp_poster, 'JPEG')
                temp_poster.seek(0)
                new_season.poster_large.save(
                                         posters['poster_large'][0] + '.jpg',
                                         ContentFile(temp_poster.read()),
                                         save=False)
                temp_poster.close()
                temp_poster = BytesIO()
                posters['poster_small'][1].save(temp_poster, 'JPEG')
                temp_poster.seek(0)
                new_season.poster_small.save(
                                         posters['poster_small'][0] + '.jpg',
                                         ContentFile(temp_poster.read()),
                                         save=False)
                temp_poster.close()
            new_season.save()
            for episode in full_season['episodes']:
                new_episode = models.Episode(name=episode['name'],
                                             air_date=episode['air_date'],
                                             tmdb_id=episode['id'],
                                             overview=episode['overview'],
                                             number=episode['episode_number'],
                                             series=new_series,
                                             season=new_season
                                             )
                new_episode.save()
            return True
    return False


@shared_task()
def _process_full_series(full_series):
    if not full_series:
        return False
    runtime = _calc_av_episode_runtime(
        full_series['series']['episode_run_time'])
    update_values = {
        'in_production': full_series['series']['in_production'],
        'first_air_date': full_series['series']['first_air_date'],
        'last_air_date': full_series['series']['last_air_date'],
        'episode_run_time': runtime,
        'number_of_episodes': full_series['series']['number_of_episodes'],
        'number_of_seasons': full_series['series']['number_of_seasons'],
        'original_language': full_series['series']['original_language'],
        'overview': full_series['series']['overview'],
        'status': full_series['series']['status'],
        'type': full_series['series']['type']
    }
    updated_series = models.Series.objects.update_or_create(
        name=full_series['series']['name'],
        tmdb_id=full_series['series']['id'],
        defaults=update_values)
    new_series = updated_series[0]
    posters = _get_posters(poster_path=full_series['series'][
                           'poster_path'])
    if (posters and
            ('poster_large' in posters) and
            ('poster_small' in posters)):
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
    new_series.genres.set(full_series['genre_list'])
    new_series.origin_country.set(full_series['country_list'])
    for number in range(1, new_series.number_of_seasons + 1):
        _convert_season(
            new_series.tmdb_id,
            new_series.id, number, new_series)
    return True


@shared_task(ignore_result=True)
def get_full_series(result):
    tmdb_tv = TV()
    full_series = tmdb_tv.get_series_info_by_id(result['id'])
    while full_series.status in states.UNREADY_STATES:
        time.sleep(1)
    if full_series.status == states.SUCCESS:
        print('It was successfull')
        if (full_series.result and
            full_series.result['number_of_seasons'] and
            (full_series.result['number_of_seasons'] != 0) and
                full_series.result['number_of_episodes'] and
                (full_series.result['number_of_episodes'] != 0)):
            return full_series.result
    return False
