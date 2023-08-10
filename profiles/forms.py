from dataclasses import field
from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.models import User


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "picture", 'instagram',
                  'twitter', "show_articles", "show_quiz")


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",)
