from django.db import models





class Series(models.Model):

    series_name = models.CharField(max_length=255)
    language = models.CharField(max_length=2)
    overview = models.TextField()
    first_aired = models.DateTimeField('first aired')
    runtime = models.IntegerField()
    imdb_id = models.CharField(max_length=255)
    tvdb_id = models.CharField(max_length=100)
    actors = models.ManyToManyField(Person)

    class Meta:
        verbose_name = "Series"
        verbose_name_plural = "Series"

    def __str__(self):
        pass


class Season(models.Model):

    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    number = models.IntegerField()

    class Meta:
        verbose_name = "Season"
        verbose_name_plural = "Seasons"

    def __str__(self):
        pass


class Episode(models.Model):

    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    relative_number = models.IntegerField()
    absolute_number = models.IntegerField()
    overview = models.TextField()

    class Meta:
        verbose_name = "Episode"
        verbose_name_plural = "Episodes"

    def __str__(self):
        pass


class Genre(models.Model):

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        pass


class Person(models.Model):

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"

    def __str__(self):
        pass


class Network(models.Model):

    class Meta:
        verbose_name = "Network"
        verbose_name_plural = "Networks"

    def __str__(self):
        pass
