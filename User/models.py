from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    UserProfile model. Holds all information about the User.
    """
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username
