"""This file holds the views of the watchlog app."""
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.views.generic import View, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from watchlog.models import Watchlog
from tv.models import Series
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
    model = Watchlog, Series
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
    """Displays statistics about the user and all users of tellylog

    """
    model = Watchlog
    template_name = 'watchlog/stats.html'
    context_object_name = 'stats'

    def number_of_episodes(self, user_entries):
        """number of episodes the user has watched
        """
        return len(user_entries)

    def all_user_number_of_episodes(self, all_user_entries):
        """Number of episodes all users haves watched
        """
        return len(all_user_entries)

    def time_spent_watching(self, entries):
        time_total = 0
        for entry in entries:
            time_total += entry
        return str(datetime.timedelta(minutes=time_total))

    def not_included_series(self, entries):
        not_included_series = []
        for entry in entries:
            if entry not in not_included_series:
                not_included_series.append(entry)
        return not_included_series

    def favourite_genre(self, user_entries):
        genre_list = {}
        for entry in user_entries:
            if entry in genre_list:
                genre_list[entry] += 1
            else:
                genre_list[entry] = 1
        highest = 0
        favourite_genre = ()
        for entry in genre_list:
            if genre_list[entry] > highest:
                highest = genre_list[entry]
                favourite_genre = entry
        return favourite_genre

    def higest_rating(self, entries):
        rating_list = {}
        rating_counter = {}
        for entry in entries:
            if entry[0] in rating_list:
                rating_list[entry[0]] += entry[1]
                rating_counter[entry[0]] += 1
            else:
                rating_list[entry[0]] = entry[1]
                rating_counter[entry[0]] = 1
        highest = 0
        highest_rated_series = ()
        for entry in rating_list:
            rating_list[entry] = rating_list[entry] / rating_counter
            if rating_list[entry] > highest:
                highest = rating_list[entry]
                highest_rated_series = entry
        return highest_rated_series

    def most_viewed_episode(self, entries):
        most_viewed_list = {}
        most_viewed_counter = {}

        for entry in entries:
            if entry[0] in most_viewed_list:
                most_viewed_counter[entry[0]] += 1
            else:
                most_viewed_list[entry[0]] = (entry[1], entry[2],
                                              entry[3], entry[4])
                most_viewed_counter[entry[0]] = 1

        highest = 0
        most_viewed_episode = []
        extra_episodes = []

        for entry in most_viewed_list:
            if most_viewed_counter[entry] > highest:
                highest = most_viewed_counter[entry]
                most_viewed_episode = most_viewed_list[entry]
                extra_episodes = []
            elif most_viewed_counter[entry] is highest:
                extra_episodes.append(most_viewed_list[entry])


        most_viewed_episode_with_users = (
            most_viewed_episode, extra_episodes, highest)
        return most_viewed_episode_with_users

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(Stats, self).get_context_data(**kwargs)
        user_entries = Watchlog.objects.filter(user=user)
        all_user_entries = Watchlog.objects.all()
        context['number_of_episodes'] = self.number_of_episodes(
            user, user_entries)
        context['all_user_number_of_episodes'] = self.\
            all_user_number_of_episodes(all_user_entries)

        # user runtimes
        user_runtimes = Series.objects.filter(episode__watchlog__user=user).\
            exclude(episode_run_time=None).values_list(
            'episode_run_time', flat=True)
        context['time_spent'] = self.time_spent_watching(user_runtimes)
        # user episodes without runtimes
        user_runtime_exceptions = Series.objects.filter(
            episode__watchlog__user=user, episode_run_time=None).\
            values_list('name', flat=True)
        context['not_included_series'] = self.not_included_series(
            user_runtime_exceptions)

        # runtimes for all users
        all_user_runtimes = Watchlog.objects.all().exclude(
            episode__series__episode_run_time=None).values_list(
            'episode__series__episode_run_time', flat=True)

        context['all_user_time_spent'] = self.\
            time_spent_watching(all_user_runtimes)

        # favourite genre for the user
        user_favourite_genre = Watchlog.objects.filter(
            user=user).exclude(episode__series__genres=None).values_list(
            'episode__series__genres__name', flat=True)
        context['favourite_genre'] = self.favourite_genre(user_favourite_genre)

        # favourite genre all users
        all_user_favourite_genre = Watchlog.objects.all().exclude(
            episode__series__genres=None).values_list(
            'episode__series__genres__name', flat=True)

        context['all_user_favourite_genre'] = self.favourite_genre(
            all_user_favourite_genre)

        # user highest rated series
        user_highest_rated_series = Watchlog.objects.filter(
            user=user).exclude(rating=0).values_list(
            'episode__series__name', 'rating')

        context['higest_rated_series'] = self.favourite_genre(
            user_highest_rated_series)

        # user highest rated series
        all_users_highest_rated_series = Watchlog.objects.all().exclude(
            rating=0).values_list('episode__series__name', 'rating')

        context['higest_rated_series'] = self.higest_rating(
            all_users_highest_rated_series)

        all_users_most_viewed_episode = Watchlog.objects.all().values_list(
            'episode__tmdb_id', 'episode__name', 'episode__season__number',
            'episode__number', 'episode__series__name')

        context['most_viewed_ep'] = self.most_viewed_episode(
            all_users_most_viewed_episode)


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
