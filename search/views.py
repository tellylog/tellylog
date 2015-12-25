"""This file holds the views of the search app."""
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpRequest  # HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, FormView, ListView
from django.core.urlresolvers import reverse
from watson import search as watson

import tv.models as tv
import tmdbcall as tmdb
from .forms import SearchForm


class SearchView(ListView):
    http_method_names = ['get']
    query_param = "q"
    template_name = "search/search.html"
    query = ''

    def get_query_param(self):
        return self.query_param

    def get_query(self, request):
        """Parses the query from the request."""
        return request.GET.get(self.get_query_param(), "").strip()

    def get_queryset(self):
        self.query = self.get_query(self.request)
        search_res = watson.search(self.query)

        if not search_res:
            tmdb_tv = tmdb.tv.TV()
            api_series = tmdb_tv.search_for_series(self.query)
            if api_series and api_series['results']:
                for series in api_series['results']:
                    # TODO convert function
                    pass
        return search_res

    def get_context_data(self, **kwargs):
        """
        Fill up the context array.

        Args:
            **kwargs: Parameters that where given to the view.

        Returns:
            dict: Context dictionary with all values.
        """
        context = super(SearchView, self).get_context_data(**kwargs)
        context['query'] = self.query
        return context



class TestView(FormView):
    template_name = "search/test.html"
    form_class = SearchForm
    form = SearchForm()
