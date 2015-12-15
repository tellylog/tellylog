import os
from tellylog import settings
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=254)
    tmdb_id = models.IntegerField(unique=True)
    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        pass


class Country(models.Model):
    name = models.CharField(max_length=254)
    tmdb_id = models.IntegerField(unique=True)
    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countrys"

    def __str__(self):
        pass


class Series(models.Model):
    name = models.CharField(max_length=254)
    tmdb_id = models.IntegerField(unique=True)
    poster_small = models.ImageField()  # TODO Set MEDIA PATH
    poster_medium = models.ImageField()
    poster_large = models.ImageField()
    in_production = models.BooleanField()
    first_air_date = models.DateField()
    episode_run_time = models.DurationField()
    last_air_date = models.DateField()
    number_of_episodes = models.IntegerField()
    number_of_seasons = models.IntegerField()
    original_language = models.CharField(max_length=4)
    overview = models.TextField()
    status = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre)
    origin_country = models.ManyToManyField(Country)
    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Series"
        verbose_name_plural = "Series"

    def __str__(self):
        pass


class Season(models.Model):
    number = models.IntegerField()
    air_date = models.DateField()
    tmdb_id = models.IntegerField()
    poster_small = models.ImageField()
    poster_medium = models.ImageField()
    poster_large = models.ImageField()
    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Season"
        verbose_name_plural = "Seasons"

    def __str__(self):
        pass


class Episode(models.Model):
    name = models.CharField(max_length=254)
    air_date = models.DateField()
    number = models.IntegerField()
    tmdb_id = models.IntegerField()
    overview = models.TextField()
    season_id = models.ForeignKey(Season, on_delete=models.CASCADE)
    # TODE guest_stars
    # TODO crew - not shure which Field

    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Episode"
        verbose_name_plural = "Episodes"

    def __str__(self):
        pass
