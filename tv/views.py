# from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse  # HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
# from django.utils import timezone
from tv.models import Series, Season


def index(request):
    return HttpResponse("'Anderson, don’t talk out loud. You lower the " +
                        "IQ of the whole street.'-Sherlock")


class SeriesView(TemplateView):
    template_name = "tv/series.html"

    def get_context_data(self, **kwargs):
        # series = Series.
        context = super(SeriesView, self).get_context_data(**kwargs)
        context['fucker'] = int(context['series_id']) * 10
        return context
