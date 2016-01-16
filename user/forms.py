from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from django.contrib.auth.forms import PasswordChangeForm

from django import forms



class UserForm(forms.ModelForm):
    """
    UserForm form. Takes the users username, password and email-address and
    checks with the user database that username and email are unique.

    Attributes:
        password (forms.CharField): Takes the users password(hidden on page).
    """
    password = forms.CharField(widget=forms.PasswordInput())
    repassword = forms.CharField(widget=forms.PasswordInput())
    repassword.label = "Password repeat"
    repassword.help_text = "please repeat your password"
    repassword.errors = {'a': ("asf")}
    captcha = ReCaptchaField(attrs={'theme': 'clean'})
    # captcha.label = ""


    class Meta:
        """
        Meta information of the UserForm.

        Attributes:
            model: equals the existing Django user model.
            fields: which fields of that model are used.
        """
        model = User
        fields = ('username', 'email', 'password')
        labels = {
            'username': ('Username'),
            'email': ('Email'),
            'password': ('Password'),
        }
        help_texts = {
            # 'username': ('Some useful help text.'),
        }

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

    def password_repeat(self):
        password = self.cleaned_data.get('password')
        repassword = self.cleaned_data.get('repassword')
        if password is not repassword:
            raise forms.ValidationError(u'Password inputs did not match!')


class CaptchaForm(forms.Form):
    captcha = ReCaptchaField()


class PWForm(PasswordChangeForm):

    class Meta:

        form = PasswordChangeForm
        fields = ('old_password', 'new_password1', 'new_password2')
        labels = {
            'old_password': ('FUT'),
        }
