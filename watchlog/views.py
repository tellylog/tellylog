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
    def post(self, request):
        if 'kind' in request.POST and 'id' in request.POST:
            kind = request.POST['kind']
            given_id = request.POST['id']
            if 'rating' in request.POST:
                rating = request.POST['rating']
            else:
                rating = None
            user = request.user
            if kind == 'series':
                episodes = list(Episode.objects.filter(series__id=given_id))
            elif kind == 'season':
                episodes = list(Episode.objects.filter(season__id=given_id))
            elif kind == 'episode':
                episodes = list(Episode.objects.get(pk=given_id))
            else:
                return JsonResponse({'error': True})

            for episode in episodes:
                new_entry = Watchlog.objects.get_or_create(user=user,
                                                           episode=episode)
                if not new_entry[1]:
                    if((rating is not None) and (rating >= 0)):
                        new_entry[0].rating = rating
                    new_entry[0].save()
            return JsonResponse({'error': False})
        return JsonResponse({'error': True})


class Unlog(LoginRequiredMixin, View):
    def post(self, request):
        print(request.POST)
        if 'kind' in request.POST and 'id' in request.POST:
            kind = request.POST['kind']
            given_id = request.POST['id']
            user = request.user

            if kind == 'series':
                episodes = list(Episode.objects.filter(series__id=given_id))
            elif kind == 'season':
                episodes = list(Episode.objects.filter(season__id=given_id))
            elif kind == 'episode':
                episodes = list(Episode.objects.get(pk=given_id))
            else:
                return JsonResponse({'error': True})
            for episode in episodes:
                Watchlog.objects.filter(user=user, episode=episode).delete()
            return JsonResponse({'error': False})
        return JsonResponse({'error': True})
