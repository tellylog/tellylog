from django.views.generic import TemplateView
from django.http import HttpResponse


class IndexView(TemplateView):
    template_name = "main/main.html"



class AboutView(TemplateView):
    template_name = "main/about.html"
