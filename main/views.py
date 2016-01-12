from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import SignInForm
from user.forms import UserForm


class Index(TemplateView):
    """
    Index View.
    template_name : takes the given template and rendes it to the view.
    """
    template_name = "main/main.html"


class About(TemplateView):
    """
    About View.
    template_name : takes the given template and rendes it to the view.
    """
    template_name = "main/about.html"


class Dummy(TemplateView):
    """
    Index View.
    template_name : takes the given template and rendes it to the view.
    """
    template_name = "main/dummy.html"


class SignIn(TemplateView):
    """
    Index View.
    template_name : takes the given template and rendes it to the view.
    """
    template_name = "main/sign-in.html"


@login_required(login_url="/main/sign_in/")
class Overview(TemplateView):
    """
    Overview View.
    template_name : takes the given template and rendes it to the view.
    @login_required : this view can only be accessed when the user is
        logged in(signed in).
    login_url : is the url wich is taken when the user is not logged in.
    """
    template_name = "main/overview.html"
