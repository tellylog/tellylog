"""This file holds the views of the watchlist app."""
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from watchlist.models import Watchlist
from tv.models import Series


class WatchlistListView(LoginRequiredMixin, ListView):
    model = Watchlist
    template_name = 'watchlist/watchlist.html'
    context_object_name = 'wlist_list'
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        watchlist = list(Watchlist.objects.filter(
            user=user).order_by('-added'))
        return watchlist


class List(LoginRequiredMixin, View):

    def post(self, request):
        if 'id' in request.POST:
            given_id = request.POST['id']
            user = request.user
            series = Series.objects.get(pk=given_id)
            entry = Watchlist.objects.get_or_create(user=user, series=series)
            if(entry[0]):
                return JsonResponse({'error': False})
        return JsonResponse({'error': True})


class Unlist(LoginRequiredMixin, View):

    def post(self, request):
        if 'id' in request.POST:
            given_id = request.POST['id']
            user = request.user
            series = Series.objects.get(pk=given_id)
            Watchlist.objects.filter(user=user, series=series).delete()
            return JsonResponse({'error': False})
        return JsonResponse({'error': True})
