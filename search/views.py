"""This file holds the views of the search app."""
from django.http import JsonResponse
from django.views.generic import View, ListView
from django.core.urlresolvers import reverse
from watson import search as watson
from celery.result import AsyncResult
from tellylog.celery import app
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

        search_task = tasks.search_online(query=self.query)
        if search_task:
            self.task_id = search_task.task_id
        else:
            self.task_id = False
        search_res = False

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
        context['task_id'] = (self.task_id if
                              self.task_id is not None else False)
        status_url = reverse('search:status')
        status_url = self.request.build_absolute_uri(status_url)
        context['status_url'] = status_url
        result_url = reverse('search:result')
        result_url = self.request.build_absolute_uri(result_url)
        context['result_url'] = result_url
        return context


class SearchStatus(View):
    def post(self, request):
        task_id = request.POST['task_id']
        result = AsyncResult(task_id, app=app)
        response = JsonResponse({'status': result.status})
        return response


class SearchResult(View):
    """docstring for SearchResult"""
    def post(self, request):
        query = request.POST['query']
        # TODO JSON Serialize the Search results
        search_res = watson.search(query)
        if search_res.count() < 1:
            response = JsonResponse({'search_res': []})
        else:
            search_res_list = []
            for sres in search_res:
                sres = sres.object
                res = {}
                res['name'] = sres.name
                res['overview'] = sres.overview
                res['year'] = (sres.first_air_date.year if
                               sres.first_air_date else None)
                res['genres'] = sres.get_genre_list()
                try:
                    res['poster'] = sres.poster_large.url
                except ValueError:
                    res['poster'] = False
                res['url'] = sres.get_absolute_url()
                search_res_list.append(res)

            response = JsonResponse({'search_res': search_res_list})
        return response
