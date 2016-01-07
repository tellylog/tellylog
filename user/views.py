from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView

from user.forms import UserForm, SignInForm


def SignUp(request):
    """
    Function that saves the given userinfo to the user database.
    """
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render_to_response(
        'user/signUp.html',
        {'user_form': user_form, 'registered': registered}, context)


class SignIn(FormView):
    """
    Function that checks given info with the user database and if info exists
    in the database it signs the user in
    """
    form_class = SignInForm
    template_name = "user/signIn.html"


@login_required
def Logout(request):
    """
    Function that logs out a signed in user.

    @login_required: regulates the avaliability of the following function
    so only logged in users can use it
    """
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))
