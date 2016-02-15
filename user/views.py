from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy

from user.forms import UserCreateForm


class SignUp(FormView):
    template_name = 'user/signUp.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('main:overview')

    def form_valid(self, form):
        form.save()
        return super(SignUp, self).form_valid(form)


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
            return HttpResponseRedirect('/user/sign-in/')
    else:
        return render(request, 'user:sign_in', {})


class SignInView(FormView):
    """
    SignInView. redirects incoming requests
    template_name : takes the given template and rendes it to the view.
    """
    template_name = "user/sign-in.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('main:overview')


@login_required
def Logout(request):
    """
    Function that logs out a signed in user.

    @login_required: regulates the avaliability of the following function
    so only logged in users can use it
    """
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))


class Profile(LoginRequiredMixin, FormView):
    template_name = 'user/profile.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('main:overview')

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(Profile, self).form_valid(form)
