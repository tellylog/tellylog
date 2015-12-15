from django.views.generic import TemplateView
from django.http import HttpResponse


class Index(TemplateView):
    template_name = "main/main.html"


class About(TemplateView):
    template_name = "main/about.html"


class Overview(TemplateView):
        template_name = "main/overview.html"


class SignIn(TemplateView):
        template_name = "main/sign_in.html"


class SignUp(TemplateView):
        template_name = "main/sign_up.html"
