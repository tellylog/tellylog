"""Retrieving, converting and stroring TMDB series."""
import hashlib
import time
from io import BytesIO
import PIL
from tmdbcall.tv import TV
from tmdbcall.poster import Poster
from tv import models
from django.db import transaction
from django.core.files.base import ContentFile
from celery import shared_task, states


@shared_task()
def check_genres(full_series):
    """Stores new genres or gets the stored genres of the series

    Args:
        full_series (dict): Holds the full series.

    Returns:
        False: On failure
        dict: Full series with a list of the genres appended.
    """
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
def check_countrys(full_series):
    """Stores new countrys or gets the stored countrys of the series

    Args:
        full_series (dict): Holds the full series.

    Returns:
        False: On failure
        dict: Full series with a list of countrys appended
    """
    country_list = []
    if not full_series:
        return False
    if ('origin_country' in full_series['series'] and
            type(full_series['series']['origin_country']) == list):
        for country in full_series['series']['origin_country']:
            default_values = {'name': country}
            db_country = (
                models.Country.objects.get_or_create(name=country,
                                                     defaults=default_values))

            if type(db_country) is tuple:
                country_list.append(db_country[0])
            else:
                country_list.append(db_country)
    full_series['country_list'] = country_list
    return full_series


def _calc_av_episode_runtime(runtimes):
    """Calculate the average episode runtime.

    Args:
        runtimes (list): List with all runtimes

    Returns:
        None: On failure
        Integer: Average runtime.
    """
    if len(runtimes) > 0:
        return sum(runtimes) // len(runtimes)
    else:
        return None


def _get_posters(poster_path):
    """Retrieves the posters using the given poster_path

    Args:
        poster_path (str): Path to the poster

    Returns:
        False: On Failure
        dict: Large and small version of the poster.
    """
    # check if a string is given
    if type(poster_path) is str:
        # remove the slash at the beginning
        poster_path = poster_path[1:]
        tmdb_poster = Poster()
        # start the task to get the poster
        poster_result = tmdb_poster.get_poster(imagename=poster_path)
        # wait for the task to finish or fail
        while poster_result.status in states.UNREADY_STATES:
            time.sleep(0.1)
        # check if a result is retrieved
        if poster_result.result and 'data' in poster_result.result:
            poster_result = poster_result.result
            # create an PIL image from bytes
            poster_large = PIL.Image.frombytes(
                data=poster_result['data'],
                size=poster_result['size'],
                mode=poster_result['mode'])
            if poster_large:
                # set the size for the small poster
                size = (180, 270)
                # resize the poster
                poster_small = poster_large.resize(size, PIL.Image.ANTIALIAS)
                # a dict with a hash and the data of both posters
                return {'poster_large': (hashlib.md5(
                                         poster_large.tobytes()).hexdigest(),
                                         poster_large),
                        'poster_small': (hashlib.md5(
                                         poster_small.tobytes()).hexdigest(),
                                         poster_small)}
    return False


@transaction.atomic
def _convert_season(tmdb_series_id, season_number, new_series):
    """Retrieve, convert and store a season of the series with it's episodes

    Args:
        tmdb_series_id (int): TMDB ID of the series
        season_number (int): Number of the season to be converted
        new_series (Series): Tellylog series the season belongs to

    Returns:
        False:  on failure
        True: on success
    """
    tmdb_tv = TV()
    # start the task to get the full season
    full_season = tmdb_tv.get_season_info_by_number(tmdb_series_id,
                                                    season_number)
    # wait for the task to finish or fail
    while full_season.status in states.UNREADY_STATES:
        time.sleep(0.1)
    # if the task succeded
    if full_season.status == states.SUCCESS:
        full_season = full_season.result
        if full_season:
            # set a dict of update values
            update_values = {
                'air_date': full_season['air_date'],
                'name': full_season['name'],
                'episode_count': len(full_season['episodes'])
            }
            # use update or create to store or update the season
            updated_season = models.Season.objects.update_or_create(
                number=season_number,
                tmdb_id=full_season['id'],
                series=new_series,
                defaults=update_values)
            # get the updated_season from the tupel
            new_season = updated_season[0]
            # check if a poster is already present
            if not new_season.poster_large:
                posters = _get_posters(poster_path=full_season['poster_path'])
            # a poster is already present - set posters to False
            else:
                posters = False
            # check if posters equals to True
            # and if the posters are in the dict
            if (posters and
                ('poster_large' in posters) and
                    ('poster_small' in posters)):
                # create a temporary poster in the cache
                temp_poster = BytesIO()
                # save the large poster in the temporary poster
                posters['poster_large'][1].save(temp_poster, 'JPEG')
                # set the offset to the beginning of the temp poster
                temp_poster.seek(0)
                # save the poster in the season with the hash as filename
                new_season.poster_large.save(
                    posters['poster_large'][0] + '.jpg',
                    ContentFile(temp_poster.read()),
                    save=False)
                # close the temp poster
                temp_poster.close()
                # repeat the process with the small poster
                temp_poster = BytesIO()
                posters['poster_small'][1].save(temp_poster, 'JPEG')
                temp_poster.seek(0)
                new_season.poster_small.save(
                    posters['poster_small'][0] + '.jpg',
                    ContentFile(temp_poster.read()),
                    save=False)
                temp_poster.close()
            # save the whole season
            new_season.save()
            # convert and store every episode
            for episode in full_season['episodes']:
                # values that are updated or filled
                update_episode_values = {
                    'name': episode['name'],
                    'air_date': episode['air_date'],
                    'overview': episode['overview'],
                }
                # update or create an episode
                models.Episode.objects.update_or_create(
                    tmdb_id=episode['id'],
                    number=episode['episode_number'],
                    series=new_series,
                    season=new_season,
                    defaults=update_episode_values)
            return True
    return False


@shared_task
@transaction.atomic
def process_full_series(full_series):
    """Retrieve, convert and store a series with it's seasons and episodes

    Args:
        full_series (dict): Holds the whole series.

    Returns:
        False: On failure
        True: On success
    """
    if not full_series:
        return False
    # calculate the average runtime
    runtime = _calc_av_episode_runtime(
        full_series['series']['episode_run_time'])
    # check if an overview is given
    if (full_series['series']['overview'] == 'null' or
            full_series['series']['overview'] is None):
        # set the overview to an empty string
        full_series['series']['overview'] = ''
    # values of the series to get updated or filled
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
    # update or create the series
    updated_series = models.Series.objects.update_or_create(
        name=full_series['series']['name'],
        tmdb_id=full_series['series']['id'],
        defaults=update_values)
    # get the series out of the tupel
    new_series = updated_series[0]
    # check if a poster is already present
    if not new_series.poster_large:
        posters = _get_posters(poster_path=full_series['series'][
                               'poster_path'])
    # a poster is already present - set posters to False
    else:
        posters = False
    # check if posters equals to True
    # and if the posters are in the dict
    if (posters and
            ('poster_large' in posters) and
            ('poster_small' in posters)):
        # create a temporary poster in the cache
        temp_poster = BytesIO()
        # save the large poster in the temporary poster
        posters['poster_large'][1].save(temp_poster, 'JPEG')
        # set the offset to the beginning of the temp poster
        temp_poster.seek(0)
        # save the poster in the series with the hash as filename
        new_series.poster_large.save(posters['poster_large'][0] + '.jpg',
                                     ContentFile(temp_poster.read()),
                                     save=False)
        # close the temp poster
        temp_poster.close()
        # repeat the process with the small poster
        temp_poster = BytesIO()
        posters['poster_small'][1].save(temp_poster, 'JPEG')
        temp_poster.seek(0)
        new_series.poster_small.save(posters['poster_small'][0] + '.jpg',
                                     ContentFile(temp_poster.read()),
                                     save=False)
        temp_poster.close()
    # save the whole series
    new_series.save()
    # set the genres of the series
    new_series.genres.set(full_series['genre_list'])
    # set the countrys of the series
    new_series.origin_country.set(full_series['country_list'])
    # convert all seasons of the series
    for number in range(1, new_series.number_of_seasons + 1):
        _convert_season(
            new_series.tmdb_id, number, new_series)
    return True


@shared_task(ignore_result=True)
def get_full_series(result):
    """ Retrieves the full series via id from tmdb.

    Args:
        result (dict): Search result from tmdb.

    Returns:
        False: On failure
        dict: Full series if successfull
    """
    tmdb_tv = TV()
    # start the task to get the full series from tmdb
    full_series = tmdb_tv.get_series_info_by_id(result['id'])
    # wait for the task to finish or fail
    while full_series.status in states.UNREADY_STATES:
        time.sleep(0.1)
    # if the task exited successfull
    if full_series.status == states.SUCCESS:
        # the series has seasons and episodes
        if (full_series.result and
            full_series.result['number_of_seasons'] and
            (full_series.result['number_of_seasons'] != 0) and
                full_series.result['number_of_episodes'] and
                (full_series.result['number_of_episodes'] != 0)):
            return full_series.result
    return False
