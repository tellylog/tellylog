from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.contrib.auth.forms import UserCreationForm



class UserCreateForm(UserCreationForm):
    captcha = ReCaptchaField()
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

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
