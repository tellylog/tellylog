from django.db import models
from django.contrib.auth import models as user
from tv import models as tv


class Watchlist(models.Model):
    user = models.ForeignKey(user.User, on_delete=models.CASCADE)
    series = models.ForeignKey(tv.Series, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Watchlist"
        verbose_name_plural = "Watchlists"
        ordering = ['-added']
        unique_together = ('series', 'user',)

    def __str__(self):
        return '%s - %s' % (self.user.username, self.series.name)
