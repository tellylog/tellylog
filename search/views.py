"""This file holds the views of the search app."""
from django.http import JsonResponse
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from watson import search as watson
from celery.result import AsyncResult
from tellylog.celery import app
import search.tasks as tasks


class SearchView(LoginRequiredMixin, TemplateView):
    """View for the search

    Attributes:
        http_method_names (list): Allowed http methodes, only get is allowed
        query (str): Query
        query_param (str): GET parameter for the query
        task_id (str, bool): ID of the search task or False if no results
        template_name (str): Name of the template to render
    """
    http_method_names = ['get']
    query_param = "q"
    template_name = "search/search.html"
    query = ''

    def get_query_param(self):
        """Get the query parameter

        Returns:
            str: Query parameter
        """
        return self.query_param

    def get_query(self, request):
        """Parses the query from the request.

        Args:
            request (object): HTTPRequest
        """
        return request.GET.get(self.get_query_param(), "").strip()

    def start_search(self):
        """Start tmdb search

        Returns:
            bool: False on failure or if nothing was found
            str: Task ID of the search task
        """
        # start the search task
        search_task = tasks.search_online(query=self.query)
        # search task equals to True
        if search_task:
            # get task id of search task
            task_id = search_task.task_id
        else:
            # set task id to false
            task_id = False
        return task_id

    def get_context_data(self, **kwargs):
        """
        Fill up the context array.

        Args:
            **kwargs: Parameters that where given to the view.

        Returns:
            dict: Context dictionary with all values.
        """
        # get the query
        self.query = self.get_query(self.request)
        # set the task id and start the search
        self.task_id = self.start_search()
        # get the existing values of the context array
        context = super(SearchView, self).get_context_data(**kwargs)
        context['query'] = self.query
        context['task_id'] = (self.task_id if
                              self.task_id is not None else False)
        # url to make ajax call to SearchStatus View
        status_url = reverse('search:status')
        status_url = self.request.build_absolute_uri(status_url)
        context['status_url'] = status_url
        # url to make ajax call to SearchResult View
        result_url = reverse('search:result')
        result_url = self.request.build_absolute_uri(result_url)
        context['result_url'] = result_url
        return context


class SearchStatus(LoginRequiredMixin, View):
    """Returns a JSON response with the status of the task

    Attributes:
        http_method_names (list): Allowed http methodes, only post is allowed
    """
    http_method_names = ['post']

    def post(self, request):
        """Return a JSON response with the status of the task

        Args:
            request (object): HTTPRequest object

        Returns:
            object: JsonResponse with the status of the task
        """
        # get the task id from the request
        task_id = request.POST['task_id']
        # get the task via id
        result = AsyncResult(task_id, app=app)
        response = JsonResponse({'status': result.status})
        return response


class SearchResult(LoginRequiredMixin, View):
    """Returns a Json response of a search query

    Attributes:
        http_method_names (list): Allowed http methodes, only post is allowed
    """
    http_method_names = ['post']

    def post(self, request):
        """Returns a Json response of a search query

        Args:
            request (object): HTTPRequest

        Returns:
            object: JsonResponse
        """
        # get query out of request
        query = request.POST['query']
        # search for the query in the database
        search_res = watson.search(query)
        # no search results
        if search_res.count() < 1:
            response = JsonResponse({'search_res': []})
        # search results
        else:
            # list of the search results
            search_res_list = []
            # go through all search results and add them to the list
            for sres in search_res:
                # set the sres to the real result
                sres = sres.object
                # result dict
                res = {}
                # set the values of the res to the sres
                res['name'] = sres.name
                res['overview'] = sres.overview
                res['year'] = (sres.first_air_date.year if
                               sres.first_air_date else None)
                res['genres'] = sres.get_genre_list()
                # try to get the poster url
                try:
                    res['poster'] = sres.poster_large.url
                # no poster is present
                except ValueError:
                    res['poster'] = False
                # url of the series
                res['url'] = sres.get_absolute_url()
                # add the result dict to the search result list
                search_res_list.append(res)
            response = JsonResponse({'search_res': search_res_list})
        return response
