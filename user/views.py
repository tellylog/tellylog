from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
import tellylog.settings as settings
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from user.forms import UserForm, CaptchaForm



def SignUp(request):
    """
    Function that saves the given userinfo to the user database.
    """
    context = RequestContext(request)
    context['recaptcha'] = settings.RECAPTCHA_PUBLIC_KEY
    registered = False
    captcha = CaptchaForm()

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        if user_form.is_valid() and password == repassword:
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect('/overview/')
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render_to_response(
        'user/signUp.html',
        {'user_form': user_form, 'registered': registered}, context)


def SignIn(request):
    """
    Function that checks given info with the user database and if info exists
    in the database it signs the user in
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect('/overview/')
        else:
            return HttpResponseRedirect('/sign-in/')
            print("Invalid login details.")
    else:
        return render(request, 'user:sign_in', {})


@login_required
def Logout(request):
    """
    Function that logs out a signed in user.

    @login_required: regulates the avaliability of the following function
    so only logged in users can use it
    """
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))


class Profile(LoginRequiredMixin, TemplateView):
        model = User
        template_name = 'user/profile.html'

        def post(request):
            oldpw = request.POST.get('oldpw')
            new_pw1 = request.POST.get('new_pw1')
            new_pw2 = request.POST.get('new_pw2')
            password = authenticate(password=oldpw)
            if password and (new_pw1 is new_pw2):
                User.set_password(new_pw1)
                User.save()
                return HttpResponseRedirect('/overview/')
            else:
                return HttpResponseRedirect('/sign-in/')
