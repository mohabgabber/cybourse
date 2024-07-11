from django import forms
from django.forms import ModelForm
from .models import ProposedArticles
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class CaptchaForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
        attrs={
            'data-theme': 'dark',
        }))


class ProposeForm(ModelForm):
    class Meta:
        model = ProposedArticles
        fields = ("content", "title", "description", "subject")

# class CommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ("content",)
