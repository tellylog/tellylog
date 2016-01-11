from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from django import forms


class UserForm(forms.ModelForm):
    """
    UserForm form. Takes the users username, password and email-address and
    checks with the user database that username and email are unique.

    Attributes:
        password (forms.CharField): Takes the users password(hidden on page).
    """
    password = forms.CharField(widget=forms.PasswordInput())
    captcha = ReCaptchaField()

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


class CaptchaForm(forms.Form):
    captcha = ReCaptchaField()
