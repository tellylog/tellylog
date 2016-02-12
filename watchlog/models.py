"""Models of the Watchlog app"""
from django.db import models
from django.contrib.auth import models as auth_user
from tv import models as tv


class Watchlog(models.Model):
    """Watchlog model

    Attributes:
        added (models.DateTimeField): Time added
        episode (models.ForeignKey): Episode
        rating (models.PositiveSmallIntegerField): Rating of the episode
        user (models.ForeignKey): User
    """
    user = models.ForeignKey(auth_user.User, on_delete=models.CASCADE)
    episode = models.ForeignKey(tv.Episode, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta information of the Watchlog.

        Attributes:
            ordering (list): Ordering of entries by values in list
            unique_together (tuple): Entries that have to be unique
            verbose_name (str): Human readable name
            verbose_name_plural (str): Human readable name plural
        """
        verbose_name = "Watchlog"
        verbose_name_plural = "Watchlogs"
        ordering = ['-added']
        unique_together = ('episode', 'user',)

    def __str__(self):
        """Return a string representation of the Watchlog.

        Returns:
            str: username: seriesname season_number/episode_number
        """
        return '%s: %s %d/%d' % (self.user.username, self.episode.series.name,
                                 self.episode.season.number,
                                 self.episode.number)
