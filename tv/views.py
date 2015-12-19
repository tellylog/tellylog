from django.shortcuts import get_object_or_404, get_list_or_404
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
        context = super(SeriesView, self).get_context_data(**kwargs)
        context['series'] = get_object_or_404(Series, pk=context['series_id'])
        context['seasons'] = get_list_or_404(Season,
                                             series_id=context['series_id'])
        return context
