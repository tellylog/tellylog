from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import SignInForm
from User.forms import UserForm
from User.models import UserProfile


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


class SignUp(TemplateView):
    template_name = "main/sign_up.html"
    user_forms = UserForm
