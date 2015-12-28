from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import SignInForm
from user.forms import UserForm


class Index(FormView):
    template_name = "main/main.html"
    form_class = SignInForm
    success_url = '/about/'


class About(TemplateView):
    template_name = "main/about.html"


class Overview(TemplateView):
    template_name = "main/overview.html"


class SignIn(TemplateView):
    template_name = "main/sign_in.html"


class SignUp(FormView):
    template_name = "user/signUp.html"
    form_class = UserForm