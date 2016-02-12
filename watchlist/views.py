"""This file holds the views of the watchlist app."""
from django.http import JsonResponse
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from watchlist.models import Watchlist
from tv.models import Series


class WatchlistListView(LoginRequiredMixin, ListView):
    """List all Watchlist entries of an user

    Attributes:
        context_object_name (str): Name of the queryset
        model (Watchlist): Model used for the query
        paginate_by (int): Entries per page
        template_name (str): Name of the template
    """
    model = Watchlist
    template_name = 'watchlist/watchlist.html'
    context_object_name = 'wlist_list'
    paginate_by = 12

    def get_queryset(self):
        """Get the list of entries

        Returns:
            list: List of all entries belonging to the current user
        """
        user = self.request.user
        watchlist = list(Watchlist.objects.filter(
            user=user).order_by('-added'))
        return watchlist


class List(LoginRequiredMixin, View):
    """Add a series to the Watchlist

    Attributes:
        http_method_names (list): Allowed http methodes, only POST
    """
    http_method_names = ['post']

    def post(self, request):
        """Handles post request to add series to the Watchlist

        Args:
            request (HTTPRequest): Request

        Returns:
            JsonResponse: Response with error true or false
        """
        # id is in the POST dict
        if 'id' in request.POST:
            given_id = request.POST['id']
            user = request.user
            series = Series.objects.get(pk=given_id)
            # get or create the entry to avoid duplicates
            entry = Watchlist.objects.get_or_create(user=user, series=series)
            # entry is present - no error
            if(entry[0]):
                return JsonResponse({'error': False})
        return JsonResponse({'error': True})


class Unlist(LoginRequiredMixin, View):
    """Remove a series from the Watchlist

    Attributes:
        http_method_names (list): Allowed http methodes, only POST
    """
    http_method_names = ['post']

    def post(self, request):
        """Handles post request to remove series from the Watchlist

        Args:
            request (HTTPRequest): Request

        Returns:
            JsonResponse: Response with error true or false
        """
        # id is in the POST request
        if 'id' in request.POST:
            given_id = request.POST['id']
            user = request.user
            series = Series.objects.get(pk=given_id)
            # delete the entry
            Watchlist.objects.filter(user=user, series=series).delete()
            # no error
            return JsonResponse({'error': False})
        return JsonResponse({'error': True})
