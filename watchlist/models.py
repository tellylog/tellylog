"""Models of the Watchlist app"""
from django.db import models
from django.contrib.auth import models as auth_user
from tv import models as tv


class Watchlist(models.Model):
    """Watchlist model

    Attributes:
        added (models.DateTimeField): Time added
        series (models.ForeignKey): Series
        user (models.ForeignKey): User
    """
    user = models.ForeignKey(auth_user.User, on_delete=models.CASCADE)
    series = models.ForeignKey(tv.Series, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta information of the Watchlist.

        Attributes:
            ordering (list): Ordering of entries by values in list
            unique_together (tuple): Entries that have to be unique
            verbose_name (str): Human readable name
            verbose_name_plural (str): Human readable name plural
        """
        verbose_name = "Watchlist"
        verbose_name_plural = "Watchlists"
        ordering = ['-added']
        unique_together = ('series', 'user',)

    def __str__(self):
        """Return a string representation of the Watchlist.

        Returns:
            str: username - seriesname
        """
        return '%s - %s' % (self.user.username, self.series.name)
