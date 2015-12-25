from django import forms
from User.models import UserProfile


class SignInForm(forms.ModelForm):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.HiddenInput(), initial=0)
