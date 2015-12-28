from django import forms
from user.models import UserProfile


class SignInForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(
        max_length=128, widget=forms.HiddenInput(), initial=0)
