"""This file holds the views of the watchlog app."""
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.views.generic import View, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from watchlog.models import Watchlog
from tv.models import Episode
import datetime


class WatchlogListView(LoginRequiredMixin, ListView):
    """List all watchlog series entries of an user

    Attributes:
        context_object_name (str): Name of the queryset
        model (Watchlog): Model used for the query
        paginate_by (int): Entries per page
        template_name (str): Name of the template
    """
    model = Watchlog
    template_name = 'watchlog/watchlog.html'
    context_object_name = 'wlog_list'
    paginate_by = 12

    def get_queryset(self):
        """Get the list of entries

        Returns:
            list: Watchlog entries
        """
        user = self.request.user
        watchlog = list(Watchlog.objects.filter(
            user=user).order_by(
            'episode__series', '-added').distinct('episode__series'))
        # sort the entries by the date added
        watchlog.sort(key=lambda x: x.added, reverse=True)
        return watchlog


class Stats(LoginRequiredMixin, TemplateView):
    model = Watchlog
    template_name = 'watchlog/stats.html'
    context_object_name = 'stats'

    def get_context_data1(self, **kwargs):
        user = self.request.user
        context = super(Stats, self).get_context_data(**kwargs)

        """Number of episodes
        """
        context['number_of_episodes'] = Watchlog.objects.filter(
            user=user).count()
        context['all_user_number_of_episodes'] = Watchlog.objects.all().count()
        return context

    def get_context_data2(self, **kwargs):
        user = self.request.user
        context = super(Stats, self).get_context_data(**kwargs)
        """Time spent watching espisode per user
        if a series does not have a runtime, it is not added up and the
        series is given to the user
        """
        runtime_counter = 0  # couter of runtime
        not_included_series = []  # array that takes the not included series

        for entry_a in Watchlog.objects.filter(user=user):
            # loops though entries to find series without runtimes
            if entry_a.episode.series.episode_run_time is not None:
                runtime_counter += entry_a.episode.series.episode_run_time
            else:
                if entry_a.episode.series.name not in not_included_series:
                    not_included_series.append(entry_a.episode.series.name)

        context['not_included_series'] = not_included_series
        context['time_spent'] = str(datetime.timedelta(
            minutes=runtime_counter))
        return context

    def get_context_data3(self, **kwargs):
        user = self.request.user
        context = super(Stats, self).get_context_data(**kwargs)
        """time spent all users together
        """
        all_user_runtime_counter = 0
        for entry in Watchlog.objects.all():
            if entry.episode.series.episode_run_time is not None:
                all_user_runtime_counter += entry.\
                    episode.series.episode_run_time
        context['total_time_spent'] = str(datetime.timedelta(
            minutes=all_user_runtime_counter))
        return context

    def get_context_data4(self, **kwargs):
        user = self.request.user
        context = super(Stats, self).get_context_data(**kwargs)
        """user top Genre
        """
        genre_list = {}
        for entry_a in Watchlog.objects.filter(user=user):
            for entry_b in entry_a.episode.series.get_genre_list():
                if entry_b['name'] in genre_list:
                    genre_list[entry_b['name']] += 1
                else:
                    genre_list[entry_b['name']] = 1
        highest = 0
        favourite_genre = 'genre'
        for key in genre_list:
            if genre_list[key] > highest:
                highest = genre_list[key]
                favourite_genre = key
        context['favourite_genre'] = favourite_genre
        """all users top Genre
        """
        all_user_genre_list = {}
        for entry_a in Watchlog.objects.all():
            for entry_b in entry_a.episode.series.get_genre_list():
                if entry_b['name'] in all_user_genre_list:
                    all_user_genre_list[entry_b['name']] += 1
                else:
                    all_user_genre_list[entry_b['name']] = 1
        all_user_highest = 0
        all_user_favourite_genre = 'genre'
        for key in all_user_genre_list:
            if all_user_genre_list[key] > all_user_highest:
                all_user_highest = genre_list[key]
                all_user_favourite_genre = key
        context['all_user_favourite_genre'] = all_user_favourite_genre
        return context


class Log(LoginRequiredMixin, View):
    """Add a series to the Watchlog

    Attributes:
        http_method_names (list): Allowed http methodes, only POST
    """
    http_method_names = ['post']

    def post(self, request):
        """Handles post request to add elements to the Watchlog

        Args:
            request (HTTPRequest): Request

        Returns:
            JsonResponse: Response with error true or false
        """
        if 'kind' in request.POST and 'id' in request.POST:
            kind = request.POST['kind']
            given_id = request.POST['id']
            if 'rating' in request.POST:
                rating = request.POST['rating']
            else:
                rating = 0
            user = request.user
            # a series is logged
            if kind == 'series':
                # get ids of all episodes of the series that are already logged
                wlog_entrys = list(
                    Watchlog.objects.filter(
                        user=user,
                        episode__series_id=given_id
                    ).values_list('episode_id', flat=True))
                # get list of all episodes of the series,
                # excluding already logged ones
                episodes = list(
                    Episode.objects.filter(
                        series__id=given_id).exclude(id__in=wlog_entrys))
            # a season is logged
            elif kind == 'season':
                # get ids of all episodes of the season that are already logged
                wlog_entrys = list(
                    Watchlog.objects.filter(
                        user=user,
                        episode__season_id=given_id
                    ).values_list('episode_id', flat=True))
                # get list of all episodes of the season,
                # excluding already logged ones
                episodes = list(
                    Episode.objects.filter(
                        season__id=given_id).exclude(id__in=wlog_entrys))
            # a episode is logged
            elif kind == 'episode':
                # try to get the watchlog entry of the episode
                wlog_entrys = Watchlog.objects.filter(
                    user=user, episode_id=given_id)
                # no episode in the watchlog (good)
                if not wlog_entrys:
                    episodes = []
                    # add an Episode object to the episodes array
                    episodes.append(Episode.objects.get(pk=given_id))
            # something was not right
            else:
                return JsonResponse({'error': True})
            new_entrys = []
            # create an array with new Watchlog entries from the episodes
            for episode in episodes:
                new_entrys.append(Watchlog(user=user, episode=episode,
                                           rating=rating))
            # try to create all entries at once
            try:
                Watchlog.objects.bulk_create(new_entrys)
            except IntegrityError:
                return JsonResponse({'error': False})
            return JsonResponse({'error': False})
        return JsonResponse({'error': True})


class Unlog(LoginRequiredMixin, View):
    """Remove a series from the Watchlog

    Attributes:
        http_method_names (list): Allowed http methodes, only POST
    """
    http_method_names = ['post']

    def post(self, request):
        """Handles post request to remove elements from the Watchlog

        Args:
            request (HTTPRequest): Request

        Returns:
            JsonResponse: Response with error true or false
        """
        if 'kind' in request.POST and 'id' in request.POST:
            kind = request.POST['kind']
            given_id = request.POST['id']
            user = request.user
            # a series is unlogged
            if kind == 'series':
                # get all episode ids from the series
                episodes = Episode.objects.filter(
                    series__id=given_id).values_list('id', flat=True)
            # a season is unlogged
            elif kind == 'season':
                # get all episode ids from the season
                episodes = Episode.objects.filter(
                    season__id=given_id).values_list('id', flat=True)
            # a episode is unlogged
            elif kind == 'episode':
                # get the id of the episode
                episode = Episode.objects.values('id').get(pk=given_id)
                episodes = [episode['id']]
            # something is not right
            else:
                return JsonResponse({'error': True})
            # delete all Watchlog entries with the episode
            Watchlog.objects.filter(user=user, episode__in=episodes).delete()
            return JsonResponse({'error': False})
        return JsonResponse({'error': True})
