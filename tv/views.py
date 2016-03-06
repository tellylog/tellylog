"""This file holds the views of the tv app."""
from django.db.models import Count, Avg
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from tv.models import Series, Season, Episode
from watchlog.models import Watchlog
from watchlist.models import Watchlist


class SeriesView(TemplateView):
    """
    Series view. Gets a Series and a list of its Seasons.

    Attributes:
        template_name (str): Which template to use.
    """

    template_name = "tv/series.html"

    def get_wlog_log_url(self):
        return self.request.build_absolute_uri(reverse('wlog:log'))

    def get_wlog_unlog_url(self):
        return self.request.build_absolute_uri(reverse('wlog:unlog'))

    def get_wlog_rate_url(self):
        return self.request.build_absolute_uri(reverse('wlog:rate'))

    def get_wlog_calc_rating_url(self):
        return self.request.build_absolute_uri(reverse('wlog:calc_rating'))

    def get_wlist_list_url(self):
        return self.request.build_absolute_uri(reverse('wlist:list'))

    def get_wlist_unlist_url(self):
        return self.request.build_absolute_uri(reverse('wlist:unlist'))

    def get_context_data(self, **kwargs):
        """
        Fill up the context array.

        Args:
            **kwargs: Parameters that where given to the view.

        Returns:
            dict: Context dictionary with all values.
        """
        context = super(SeriesView, self).get_context_data(**kwargs)
        context['series'] = \
            get_object_or_404(Series, pk=context['series_id'])
        seasons = get_list_or_404(Season,
                                  series_id=context['series_id'],
                                  episode_count__gt=0)
        context['seasons'] = list()
        avg_rating = Watchlog.objects \
            .filter(user_id=self.request.user.id,
                    episode__series_id=context['series'].id, rating__gt=0) \
            .aggregate(avg_rating=Avg('rating'))
        avg_rating = avg_rating['avg_rating']
        context['avg_rating'] = avg_rating
        context['wlog_count'] = 0
        for season in seasons:
            wlog_entry = {}
            wlog_entry['wlog_count'] = Watchlog.objects \
                .filter(user_id=self.request.user.id,
                        episode__season_id=season.id) \
                .aggregate(wlog_count=Count('id'))
            wlog_entry['wlog_count'] = wlog_entry['wlog_count']['wlog_count']
            wlog_entry['avg_rating'] = Watchlog.objects \
                .filter(user_id=self.request.user.id,
                        episode__season_id=season.id, rating__gt=0) \
                .aggregate(avg_rating=Avg('rating'))
            wlog_entry['avg_rating'] = wlog_entry['avg_rating']['avg_rating']

            if(wlog_entry['wlog_count'] is 0):
                wlog_entry = None
            context['seasons'].append((season, wlog_entry))
            if wlog_entry:
                context['wlog_count'] += wlog_entry['wlog_count']

        context['genre_list'] = context['series'].get_genre_list()

        try:
            context['wlist'] = Watchlist.objects.get(user=self.request.user,
                                                     series_id=context[
                                                         'series_id']
                                                     )
        except Watchlist.DoesNotExist:
            context['wlist'] = False

        # URLs for AJAX requests
        context['wlog_log_url'] = self.get_wlog_log_url()
        context['wlog_unlog_url'] = self.get_wlog_unlog_url()
        context['wlog_calc_rating_url'] = self.get_wlog_calc_rating_url()
        context['wlist_list_url'] = self.get_wlist_list_url()
        context['wlist_unlist_url'] = self.get_wlist_unlist_url()
        return context


class SeasonView(TemplateView):
    """
    Season view. Gets a Season and a list of its Episodes.

    Attributes:
        template_name (str): Which template to use.
    """

    template_name = "tv/season.html"

    def get_wlog_log_url(self):
        return self.request.build_absolute_uri(reverse('wlog:log'))

    def get_wlog_unlog_url(self):
        return self.request.build_absolute_uri(reverse('wlog:unlog'))

    def get_wlog_rate_url(self):
        return self.request.build_absolute_uri(reverse('wlog:rate'))

    def get_wlist_list_url(self):
        return self.request.build_absolute_uri(reverse('wlist:list'))

    def get_wlist_unlist_url(self):
        return self.request.build_absolute_uri(reverse('wlist:unlist'))

    def get_context_data(self, **kwargs):
        """
        Fill up the context array.

        Args:
            **kwargs: Parameters that where given to the view.

        Returns:
            dict: Context dictionary with all values.
        """
        context = super(SeasonView, self).get_context_data(**kwargs)
        context['series'] = get_object_or_404(Series, pk=context['series_id'])
        context['season'] = get_object_or_404(Season,
                                              series_id=context['series_id'],
                                              number=context['season_number'])
        episodes = get_list_or_404(Episode,
                                   series_id=context['series_id'],
                                   season_id=context['season'].id)
        context['wlog_count'] = 0
        context['episodes'] = list()
        for episode in episodes:
            try:
                wlog_entry = Watchlog.objects.get(user_id=self.request.user.id,
                                                  episode_id=episode.id)
            except Watchlog.DoesNotExist:
                wlog_entry = None
            context['episodes'].append((episode, wlog_entry))
            if wlog_entry:
                context['wlog_count'] += 1
        # URLs for AJAX requests
        context['wlog_log_url'] = self.get_wlog_log_url()
        context['wlog_unlog_url'] = self.get_wlog_unlog_url()
        context['wlog_rate_url'] = self.get_wlog_rate_url()
        return context
