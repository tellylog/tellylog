"""Holds all forms of the search app"""
from django import forms


class SearchForm(forms.Form):
    """Form for the search

    Attributes:
        q (forms.CharFiels): Field for the search query
    """
    q = forms.CharField()
