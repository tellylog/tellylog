"""This file holds the views of the watchlog app."""
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from watchlog.models import Watchlog
from tv.models import Series, Season, Episode


class WatchlogListView(LoginRequiredMixin, ListView):
    model = Watchlog
    template_name = 'watchlog/watchlog.html'
    context_object_name = 'wlog_list'
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        watchlog = list(Watchlog.objects.filter(
            user=user).order_by(
            '-added'))
        only_series = []
        for wlog_entry in watchlog:
            if wlog_entry.episode.series not in only_series:
                only_series.append(wlog_entry.episode.series)
        return only_series





class Log(LoginRequiredMixin, View):
    def post(self, request):
        if 'kind' in request.POST and 'id' in request.POST:
            kind = request.POST['kind']
            given_id = request.POST['id']
            if 'rating' in request.POST:
                rating = request.POST['rating']
            else:
                rating = 0
            user = request.user
            if kind == 'series':
                wlog_entrys = list(
                    Watchlog.objects.filter(
                        user=user,
                        episode__series_id=given_id
                        ).values_list('episode_id', flat=True))
                episodes = list(
                    Episode.objects.filter(
                           series__id=given_id).exclude(id__in=wlog_entrys))
            elif kind == 'season':
                wlog_entrys = list(
                    Watchlog.objects.filter(
                        user=user,
                        episode__season_id=given_id
                        ).values_list('episode_id', flat=True))
                episodes = list(
                    Episode.objects.filter(
                        season__id=given_id).exclude(id__in=wlog_entrys))
            elif kind == 'episode':
                wlog_entrys = Watchlog.objects.filter(
                                user=user, episode_id=given_id)
                if not wlog_entrys:
                    episodes = []
                    episodes.append(Episode.objects.get(pk=given_id))
            else:
                return JsonResponse({'error': True})
            new_entrys = []
            for episode in episodes:
                new_entrys.append(Watchlog(user=user, episode=episode,
                                           rating=rating))
            try:
                Watchlog.objects.bulk_create(new_entrys)
            except IntegrityError:
                return JsonResponse({'error': False})
            return JsonResponse({'error': False})
        return JsonResponse({'error': True})


class Unlog(LoginRequiredMixin, View):
    def post(self, request):
        if 'kind' in request.POST and 'id' in request.POST:
            kind = request.POST['kind']
            given_id = request.POST['id']
            user = request.user

            if kind == 'series':
                episodes = Episode.objects.filter(
                    series__id=given_id).values_list('id', flat=True)
            elif kind == 'season':
                episodes = Episode.objects.filter(
                    season__id=given_id).values_list('id', flat=True)
            elif kind == 'episode':
                episode = Episode.objects.values('id').get(pk=given_id)
                episodes = [episode['id']]
            else:
                return JsonResponse({'error': True})
            Watchlog.objects.filter(user=user, episode__in=episodes).delete()
            return JsonResponse({'error': False})
        return JsonResponse({'error': True})
