"""This file holds the views of the watchlog app."""
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from watchlog.models import Watchlog
from tv.models import Episode


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


class Rate(LoginRequiredMixin, View):
    """Add a rating to an episode in the Watchlog"""

    http_method_names = ['post']

    def post(self, request):
        if 'id' in request.POST and 'rating' in request.POST:
            rating = int('0' + request.POST['rating'])
            episode_id = request.POST['id']
            user = request.user
            if (rating >= -1 and rating < 5):
                wlog_entry = Watchlog.objects.filter(user=user,
                                                     episode=episode_id).get()
                wlog_entry.rating = rating + 1
                wlog_entry.save()
                return JsonResponse({'error': False})
        return JsonResponse({'error': True})
