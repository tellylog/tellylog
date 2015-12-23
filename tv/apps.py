"""This file holds the Configuration of the tv app."""
from django.apps import AppConfig


class TvConfig(AppConfig):
    """Config of the tv app.

    Attributes:
        name (str): Name of the app
    """

    name = 'tv'

    def ready(self):
        from watson import search as watson
        Series = self.get_model('Series')
        watson.register(Series,
                        fields=('name',),
                        store=('overview',))
