"""This file holds the views of the watchlog app."""
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.generic import View, ListView
from django.core.urlresolvers import reverse
from watchlog.models import Watchlog


class WatchlogListView(ListView):
    model = Watchlog
    template_name = 'watchlog/watchlog.html'
    context_object_name = 'wlog_list'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        self.watchlog = get_list_or_404(Watchlog, user=user)

