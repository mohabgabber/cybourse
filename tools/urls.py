from django.urls import path
from .views import *
urlpatterns = [
    path("ipa/keyboard/", IPAKeyboard.as_view(), name="ipa-keyboard"),
]
