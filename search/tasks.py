"""Celery tasks to search for a series in tmdb"""
import time
from celery import shared_task, chain, chord
from tv import convert
import tmdbcall as tmdb
from celery import states
from tv.models import Series


@shared_task()
def search_ready(result):
    """Is called at the end of the chord of tasks.

    Args:
        result (bool): Return values of a single chain of tasks

    Returns:
        bool: Return value of the task
    """
    return result


@shared_task()
def dummy():
    """Just returns True

    Returns:
        bool: Always True
    """
    return True


@shared_task()
def search_online(query):
    """Searches tmdb for the query and starts celery tasks

    Args:
        query (str): Search query

    Raises:
        Series.UpdateMe: The series needs an update.

    Returns:
        object: Celery task
        bool: False on failure or if no results where found
    """
    tmdb_tv = tmdb.tv.TV()
    # search task for the series
    api_series = tmdb_tv.search_for_series(query)
    # wait for the task to finish or fail
    while api_series.status in states.UNREADY_STATES:
        time.sleep(0.1)
    # check if the task exited successfull
    if api_series.status == states.SUCCESS:
        # check if there are results
        if api_series.result and api_series.result['total_results'] > 0:
            # list for the convert chained tasks
            to_convert = []
            # go through every result of the search
            for series in api_series.result['results']:
                try:
                    # try to get the series from the database
                    obj = Series.objects.get(tmdb_id=series['id'])
                    # retrieved series needs an update
                    if obj.update_needed():
                        # raise an UpdateMe exception
                        raise Series.UpdateMe('update me please')
                    # no update needed
                    else:
                        # append the dummy task to the list
                        to_convert.append(dummy.s())
                # catch the DoesNotExist error or the UpdateMe error
                except (Series.DoesNotExist, Series.UpdateMe):
                    # add a chain of tasks to the list
                    # get the full series -> check genres -> check countrys
                    # -> process full series
                    to_convert.append(chain(convert.get_full_series.s(series),
                                            convert.check_genres.s(),
                                            convert.check_countrys.s(),
                                            convert.process_full_series.s()))
            # to_convert holds tasks
            if len(to_convert) > 0:
                # make a chord out of the list of chains and call
                # search_ready when all end
                converter = chord(to_convert)(search_ready.s())
                return converter
    return False
