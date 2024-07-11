from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3


# class CaptchaForm(forms.Form):
#     captcha = ReCaptchaField(widget=ReCaptchaV3)


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password1', 'password2')

    def clean_username(self):
        username = str(self.cleaned_data.get('username'))
        lowercase_username = username.lower()
        return lowercase_username


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(max_length=150, required=True)

    # class Meta:
    #     model = User
    #     fields = ('username', 'password')


class UpdateEmail(ModelForm):
    class Meta:
        model = User
        fields = ("email",)
