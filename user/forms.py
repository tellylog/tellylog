from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.contrib.auth.forms import UserCreationForm



class UserCreateForm(UserCreationForm):
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



class CaptchaForm(forms.Form):
    captcha = ReCaptchaField()


class PWForm(PasswordChangeForm):
    class Meta:

        form = PasswordChangeForm
        fields = ('old_password', 'new_password1', 'new_password2')
        labels = {
            'old_password': ('FUT'),
        }
