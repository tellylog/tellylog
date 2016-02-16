"""This file holds the views of the tv app."""
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
        context['seasons'] = get_list_or_404(Season,
                                             series_id=context['series_id'],
                                             episode_count__gt=0)
        context['wlog'] = Watchlog.objects.filter(
            user_id=self.request.user.id,
            episode__series_id=context['series_id']).count()
        context['wlog_seasons'] = {}
        for season in context['seasons']:
            context['wlog_seasons'][season.id] = (
                Watchlog.objects.filter(user_id=self.request.user.id,
                                        episode__season_id=season.id).count())

        context['genre_list'] = context['series'].get_genre_list()
        wlog_log_url = reverse('wlog:log')
        wlog_log_url = self.request.build_absolute_uri(wlog_log_url)
        context['wlog_log_url'] = wlog_log_url
        wlog_unlog_url = reverse('wlog:unlog')
        wlog_unlog_url = self.request.build_absolute_uri(wlog_unlog_url)
        context['wlog_unlog_url'] = wlog_unlog_url
        try:
            context['wlist'] = Watchlist.objects.get(user=self.request.user,
                                                     series_id=context[
                                                         'series_id']
                                                     )
        except Watchlist.DoesNotExist:
            context['wlist'] = False
        wlist_list_url = reverse('wlist:list')
        wlist_list_url = self.request.build_absolute_uri(wlist_list_url)
        context['wlist_list_url'] = wlist_list_url
        wlist_unlist_url = reverse('wlist:unlist')
        wlist_unlist_url = self.request.build_absolute_uri(wlist_unlist_url)
        context['wlist_unlist_url'] = wlist_unlist_url
        return context


class SeasonView(TemplateView):
    """
    Season view. Gets a Season and a list of its Episodes.

    Attributes:
        template_name (str): Which template to use.
    """

    template_name = "tv/season.html"

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
        wlog_log_url = reverse('wlog:log')
        wlog_log_url = self.request.build_absolute_uri(wlog_log_url)
        context['wlog_log_url'] = wlog_log_url
        wlog_unlog_url = reverse('wlog:unlog')
        wlog_unlog_url = self.request.build_absolute_uri(wlog_unlog_url)
        context['wlog_unlog_url'] = wlog_unlog_url
        wlog_rate_url = reverse('wlog:rate')
        wlog_rate_url = self.request.build_absolute_uri(wlog_rate_url)
        context['wlog_rate_url'] = wlog_rate_url
        return context
