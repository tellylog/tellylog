"""
This file holds all forms for the main app.

"""
from django import forms
from user.models import UserProfile


class SignInForm(forms.Form):
    """
    SignInForm form. Takes the users username and password and is accessed by
    the user app to confirm if a user and password combination exists in the
    user database.

    Attributes:
        username (forms.CharField): Takes the users username.
        password (forms.CharField): Takes the users password(hidden on page).
    """
    username = forms.CharField(max_length=128)
    password = forms.CharField(
        max_length=128, widget=forms.HiddenInput(), initial=0)
