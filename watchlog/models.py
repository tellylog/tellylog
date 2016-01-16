from django.db import models
from django.contrib.auth import models as user
from tv import models as tv


class Watchlog(models.Model):
    user = models.ForeignKey(user.User, on_delete=models.CASCADE)
    episode = models.ForeignKey(tv.Episode, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Watchlog"
        verbose_name_plural = "Watchlogs"
        ordering = ['-added']
        unique_together = ('episode', 'user',)

    def __str__(self):
        return '%s: %s %d/%d' % (self.user.username, self.episode.series.name,
                                 self.episode.season.number,
                                 self.episode.number)
