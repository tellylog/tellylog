"""This file holds the views of the tv app."""
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from tv.models import Series, Season, Episode, Genre
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


class GenresView(LoginRequiredMixin, TemplateView):
    template_name = "tv/genres.html"

    def get_genres(self, entries):
        """Takes a list of genres from the database and returns a list with
        every genre just once, and sorts them alphabetically
        """
        genre_list = []
        for entry in entries:
            if entry not in genre_list:
                genre_list.append(entry)
        genre_list.sort()
        return genre_list

    def get_context_data(self, **kwargs):
        context = super(GenresView, self).get_context_data(**kwargs)

        watchlog_genres = Watchlog.objects.all().exclude(
            episode__series__genres=None).values_list(
            'episode__series__genres__name', 'episode__series__genres__tmdb_id')
        context['genres'] = self.get_genres(watchlog_genres)
        return context


class GenresSingle(LoginRequiredMixin, TemplateView):
    template_name = "tv/genres_single.html"

    def get_series_by_genre(self, entries, genre_id):
        series_list = []
        for entry in entries:
            if entry[2] is genre_id:
                series_list.append(entry)
        return series_list

    def get_context_data(self, **kwargs):
        context = super(GenresSingle, self).get_context_data(**kwargs)
        genre_id = \
            get_object_or_404(Genre, pk=context['genre_id'])

        watchlog_genres = Watchlog.objects.all().exclude(
            episode__series__genres=None).values_list(
            'episode__series__genres__name', 'episode__series_name',
            'episode_series_genres_tmdb_id')
        context['series'] = self.get_series_by_genre(watchlog_genres, genre_id)
        return context
