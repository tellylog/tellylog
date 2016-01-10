import time
from celery import shared_task, chain, chord
from tv import convert
import tmdbcall as tmdb
from celery import states


@shared_task()
def search_ready(result):
    return result


@shared_task()
def search_online(query, task_id=None):
    tmdb_tv = tmdb.tv.TV()
    api_series = tmdb_tv.search_for_series(query)
    while api_series.status in states.UNREADY_STATES:
        time.sleep(1)
    if api_series.status == states.SUCCESS:
        if api_series.result and api_series.result['total_results'] > 0:
            to_convert = []
            for series in api_series.result['results']:
                to_convert.append(chain(convert.get_full_series.s(series),
                                        convert._check_genres.s(),
                                        convert._check_countrys.s(),
                                        convert._process_full_series.s()))
            converter = chord(to_convert)(search_ready.s())
            return converter
