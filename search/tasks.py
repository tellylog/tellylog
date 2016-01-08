import time
from celery import shared_task, chain, group
from tv import convert
import tmdbcall as tmdb
from celery import states


@shared_task(ignore_result=True)
def start_converting(api_series):
    if api_series and 'results' in api_series:
        print('Start Converting')
        to_convert = []
        for series in api_series['results']:
            to_convert.append(convert.convert_series_result.s(series))
        group(to_convert)()
        return True


@shared_task(ignore_result=True)
def search_online(query):
    tmdb_tv = tmdb.tv.TV()
    api_series = tmdb_tv.search_for_series(query)
    # while api_series.status in states.UNREADY_STATES:
    #     print(api_series.status)
    #     time.sleep(1)
    start_converting.s(api_series).apply_async()
