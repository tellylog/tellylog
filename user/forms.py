from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms


class UserForm(forms.ModelForm):
    """
    UserForm form. Takes the users username, password and email-address and
    checks with the user database that username and email are unique.

    Attributes:
        password (forms.CharField): Takes the users password(hidden on page).
    """
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        """
        Meta information of the UserForm.

        Attributes:
            model: equals the existing Django user model.
            fields: which fields of that model are used.
        """
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        """
        Additional function to check if the given email adress is unique.
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(
                email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class SignInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

    def check_userdata(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect('/overview/')
        else:
            raise forms.ValidationError(
                u'username/password comination is incorrect!')
