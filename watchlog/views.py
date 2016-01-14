"""This file holds the views of the watchlog app."""
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import JsonResponse
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from watchlog.models import Watchlog
from tv.models import Series, Season, Episode


class WatchlogListView(LoginRequiredMixin, ListView):
    model = Watchlog
    template_name = 'watchlog/watchlog.html'
    context_object_name = 'wlog_list'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        watchlog = list(Watchlog.objects.filter(user__id=user.id))
        if not watchlog:
            return []
        else:
            return watchlog


class Log(LoginRequiredMixin, View):
    def post(self):
        if 'kind' in self.request.POST and 'id' in self.request.POST:
            kind = self.request.POST['kind']
            given_id = self.request.POST['id']
            rating = self.request.POST['rating']
            user = self.request.user
            if kind is 'series':
                episodes = list(Episode.objects.filter(series__id=given_id))
            elif kind is 'season':
                episodes = list(Episode.objects.filter(season__id=given_id))
            elif kind is 'episode':
                episodes = list(Episode.objects.get(pk=given_id))
            else:
                return JsonResponse({'error': True})

            for episode in episodes:
                new_entry = Watchlog(user=user, episode=episode)
                if(rating >= 0):
                    new_entry.rating = rating
                new_entry.save()
            return JsonResponse({'error': False})

        else:
            return JsonResponse({'error': True})


