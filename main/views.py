from django.views.generic.base import TemplateView
from django.shortcuts import render



class MainView(TemplateView):
    template_name = "main.html"
    """
    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        return context
    """
