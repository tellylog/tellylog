"""This file holds the views of the search app."""
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse
# from django.core.urlresolvers import reverse
from django.views.generic import View, FormView, ListView
from django.core.urlresolvers import reverse
from watson import search as watson
import tv.models as models
import tmdbcall as tmdb
from .forms import SearchForm
import search.tasks as tasks


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
            search_task = tasks.search_online.delay(query=self.query)
            self.task_id = search_task.task_id
            search_res = False
        else:
            self.task_id = False
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
        context['task_id'] = self.task_id if self.task_id else False
        return context


class SearchStatus(View):
    def post(self, request):
        status = SearchView.search_online.AsyncResut(task_id)
        response = JsonResponse({'status': status.status})
        return response


class TestView(FormView):
    template_name = "search/test.html"
    form_class = SearchForm
    form = SearchForm()