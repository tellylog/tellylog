"""This file holds the views of the tv app."""
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse  # HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
# from django.utils import timezone
from tv.models import Series, Season, Episode
from watchlog.models import Watchlog


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
                                             series_id=context['series_id'])
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
        context['episodes'] = get_list_or_404(Episode,
                                              series_id=context['series_id'],
                                              season_id=context['season'].id)
        context['wlog'] = Watchlog.objects.filter(
            user_id=self.request.user.id,
            episode__season_id=context['season'].id).count()
        context['wlog_episodes'] = {}
        for episode in context['episodes']:
            context['wlog_episodes'][episode.id] = (
                Watchlog.objects.filter(user_id=self.request.user.id,
                                        episode_id=episode.id).count())
        wlog_log_url = reverse('wlog:log')
        wlog_log_url = self.request.build_absolute_uri(wlog_log_url)
        context['wlog_log_url'] = wlog_log_url
        wlog_unlog_url = reverse('wlog:unlog')
        wlog_unlog_url = self.request.build_absolute_uri(wlog_unlog_url)
        context['wlog_unlog_url'] = wlog_unlog_url
        return context


class TestView(TemplateView):
    template_name = "tv/test.html"
