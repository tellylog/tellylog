"""This file holds all models for the tv app.

Attributes:
    TV_IMAGE_PATH (str): Path is appended to MEDIA_ROOT defined in settings
"""

from django.db import models

TV_IMAGE_PATH = 'tv/{type}/{category}/{size}'


class Person(models.Model):
    """
    Person model. Holds all information from actors, directors,...

    Attributes:
        added (models.DateTimeField): When was the Person added
        biography (models.TextField): Biography of the Person, can be blank
        birthday (models.DateField): Birthday, can be blank or null
        deathday (models.DateField): Deathday, can be blank or null
        last_update (models.DateTimeField): When was the last Update
        name (models.CharField): Name of the Person, max 254
        place_of_birth (models.CharField): Birthplace, can be blank, max 254
        profile_large (models.ImageField): Large image of Person,
                                           can be blank or null
        profile_medium (models.ImageField): Medium image of Person,
                                            can be blank or null
        profile_small (models.ImageField): Small image of Person,
                                           can be blank or null
        tmdb_id (models.IntegerField): ID of the TMDB entry
    """

    name = models.CharField(max_length=254)
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
        """
        Meta information of the Person.

        Attributes:
            verbose_name (str): Human readable Name of the Model
            verbose_name_plural (str): Human readable plural Name of the Model
        """

        verbose_name = "Person"
        verbose_name_plural = "Persons"

    def __str__(self):
        """
        Return a string representation of a Person.

        Returns:
            str: Name of the Person
        """
        return self.name


class Genre(models.Model):
    """
    Genre model. Holds information to a Genre.

    Attributes:
        added (models.DateTimeField): When was the Genre added
        last_update (models.DateTimeField): When was the Genre updated
        name (models.CharField): Name of the Genre, max 254
        tmdb_id (models.IntegerField): ID of the TMDB entry
    """

    name = models.CharField(max_length=254)
    tmdb_id = models.IntegerField(unique=True)
    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta information of the Genre.

        Attributes:
            verbose_name (str): Human readable name
            verbose_name_plural (str): Human readable name plural
        """

        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        """
        Return a string representation of the Genre.

        Returns:
            str: Name of the Genre
        """
        return self.name


class Country(models.Model):
    """
    Country model. Holds information to a Country.

    Attributes:
        added (models.DateTimeField): When was the Country added
        last_update (models.DateTimeField): When was the Country updated
        name (models.CharField): Name of the Country, max 254
    """

    name = models.CharField(max_length=254)
    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta information of the Country.

        Attributes:
            verbose_name (str): Human readable name
            verbose_name_plural (str): Human readable name plural
        """

        verbose_name = "Country"
        verbose_name_plural = "Countrys"

    def __str__(self):
        """
        Return a string representation of the Country.

        Returns:
            str: Name of the Country
        """
        return self.name


class Series(models.Model):
    """
    Series model. Holds all the data belonging to a Series.

    Attributes:
        added (models.DateTimeField): When was the Series added
        episode_run_time (models.IntegerField): How log is an episode normaly,
                                                can be blank or null
        first_air_date (models.DateField): When was the first episode aired,
                                           can be blank or null
        genres (models.ManyToManyField): Genres of the Series
        in_production (model.BooleanField): Still in production?
        last_air_date (models.DateField): When was did last episode air,
                                          can be blank or null
        last_update (models.DateTimeField): When was the Series updated
        name (models.CharField): Name of the Series, max 254
        number_of_episodes (models.IntegerField): How many episodes
        number_of_seasons (models.IntegerField): How many seasons
        origin_country (models.ManyToManyField): Origin Countrys
        original_language (models.CharField): Original Language, max 100,
                                              can be blank
        overview (models.TextField): Description of the Series
        poster_large (models.ImageField): Large poster image of Series,
                                           can be blank or null
        poster_medium (models.ImageField): Medium poster image of Series,
                                           can be blank or null
        poster_small (models.ImageField): Small poster image of Series,
                                           can be blank or null
        status (models.CharField): Status of the Series, max 100, can be blank
        tmdb_id (models.IntegerField): ID of the TMDB entry
        type (models.CharField): Type (style) of the Series, max 100,
                                 can be blank
    """

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
        """
        Meta information of the Series.

        Attributes:
            verbose_name (str): Human readable name
            verbose_name_plural (str): Human readable name plural
        """

        verbose_name = "Series"
        verbose_name_plural = "Series"

    def __str__(self):
        """Return a string representation of the Series.

        Returns:
            str: Name of the Series
        """
        return self.name


class Season(models.Model):
    """
    Season model. Holds all the data belonging to a Season of a Series.

    Attributes:
        added (models.DateTimeField): When was the Season added
        air_date (models.DateField): When did the Season first air
        episode_count (models.IntegerField): How many Episodes
        last_update (models.DateTimeField): When was the Season updated
        number (models.IntegerField): Number of the Season
        poster_large (models.ImageField): Large poster image of Season,
                                           can be blank or null
        poster_medium (models.ImageField): Medium poster image of Season,
                                           can be blank or null
        poster_small (models.ImageField): Small poster image of Season,
                                           can be blank or null
        series_id (models.ForeignKey): Series the Season belongs to
        tmdb_id (models.IntegerField): ID of the TMDB entry
    """

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
        """
        Meta information of the Season.

        Attributes:
            verbose_name (str): Human readable name
            verbose_name_plural (str): Human readable name plural
        """

        verbose_name = "Season"
        verbose_name_plural = "Seasons"

    def __str__(self):
        """
        Return a string representation of the Season.

        Returns:
            str: Name of the Series + Number of Season
        """
        return '%s %d' % (self.series_id.name, self.number)


class Episode(models.Model):
    """
    Episode model. Holds all the data belonging to a Episode of a Season.

    Attributes:
        added (models.DateTimeField): When was the Episode added
        air_date (models.DateField): When did the Episode first air
        last_update (models.DateTimeField): When was the Episode updated
        name (models.CharField): Name of the episode, max 254, can be blank
        number (models.IntegerField): Number of the episode
        overview (models.TextField): Description of the Episode
        season_id (models.ForeignKey): Season the Episode belongs to
        series_id (models.ForeignKey): Series the Episode belongs to
        tmdb_id (models.IntegerField): ID of the TMDB entry
    """

    name = models.CharField(max_length=254, blank=True)
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
        """
        Meta information of the Episode.

        Attributes:
            verbose_name (str): Human readable name
            verbose_name_plural (str): Human readable name plural
        """

        verbose_name = "Episode"
        verbose_name_plural = "Episodes"

    def __str__(self):
        """
        Return a string representation of the Episode.

        Returns:
            str: Name of the Series + Number of Season + Number of Episode
        """
        return '%s Season %d Ep %d' % (self.series_id.name,
                                       self.season_id.number,
                                       self.number)
