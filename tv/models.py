from django.db import models

TV_IMAGE_PATH = 'tv/{type}/{category}/{size}'


class Person(models.Model):
    name = models.CharField(max_length=254)
    also_known_as = models.TextField(blank=True)  # Stores a List as JSON
    biography = models.TextField(blank=True)
    birthday = models.DateField(blank=True, null=True)
    deathday = models.DateField(blank=True, null=True)
    tmdb_id = models.IntegerField()
    place_of_birth = models.CharField(max_length=254, blank=True)
    profile_small = models.ImageField(
        upload_to=TV_IMAGE_PATH.format(type='profile',
                                       category='person', size='small'),
        max_length=254, blank=True, null=True)
    profile_medium = models.ImageField(
        upload_to=TV_IMAGE_PATH.format(type='profile',
                                       category='person', size='medium'),
        max_length=254, blank=True, null=True)
    profile_large = models.ImageField(
        upload_to=TV_IMAGE_PATH.format(type='profile',
                                       category='person', size='large'),
        max_length=254, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"

    def __str__(self):
        pass

    # TODO Methode to get and set also_known_as with auto JSON


class Genre(models.Model):
    name = models.CharField(max_length=254)
    tmdb_id = models.IntegerField(unique=True)
    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=254)
    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countrys"

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=254)
    tmdb_id = models.IntegerField(unique=True)
    poster_small = models.ImageField(
        upload_to=TV_IMAGE_PATH.format(type='poster',
                                       category='series', size='small'),
        max_length=254, blank=True, null=True)
    poster_medium = models.ImageField(
        upload_to=TV_IMAGE_PATH.format(type='poster',
                                       category='series', size='medium'),
        max_length=254, blank=True, null=True)
    poster_large = models.ImageField(
        upload_to=TV_IMAGE_PATH.format(type='poster',
                                       category='series', size='large'),
        max_length=254, blank=True, null=True)
    in_production = models.BooleanField()
    first_air_date = models.DateField(blank=True, null=True)
    episode_run_time = models.DurationField(blank=True, null=True)
    last_air_date = models.DateField(blank=True, null=True)
    number_of_episodes = models.IntegerField()
    number_of_seasons = models.IntegerField()
    original_language = models.CharField(max_length=4, blank=True)
    overview = models.TextField(blank=True)
    status = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=100, blank=True)
    genres = models.ManyToManyField(Genre)
    origin_country = models.ManyToManyField(Country)
    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Series"
        verbose_name_plural = "Series"

    def __str__(self):
        return self.name


class Season(models.Model):
    number = models.IntegerField()
    air_date = models.DateField()
    tmdb_id = models.IntegerField()
    episode_count = models.IntegerField()
    poster_small = models.ImageField(
        upload_to=TV_IMAGE_PATH.format(type='poster',
                                       category='season', size='small'),
        max_length=254, blank=True, null=True)
    poster_medium = models.ImageField(
        upload_to=TV_IMAGE_PATH.format(type='poster',
                                       category='season', size='medium'),
        max_length=254, blank=True, null=True)
    poster_large = models.ImageField(
        upload_to=TV_IMAGE_PATH.format(type='poster',
                                       category='season', size='large'),
        max_length=254, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    series_id = models.ForeignKey(Series, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Season"
        verbose_name_plural = "Seasons"

    def __str__(self):
        return '%s %d' % (self.series_id.name, self.number)


class Episode(models.Model):
    name = models.CharField(max_length=254)
    air_date = models.DateField(blank=True, null=True)
    number = models.IntegerField()
    tmdb_id = models.IntegerField()
    overview = models.TextField(blank=True)
    season_id = models.ForeignKey(Season, on_delete=models.CASCADE)
    series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
    # TODO guest_stars
    # TODO crew - not shure which Field

    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Episode"
        verbose_name_plural = "Episodes"

    def __str__(self):
        return '%s Season %d Ep %d' % (self.series_id.name,
                                       self.season_id.number,
                                       self.number)
