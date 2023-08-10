from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class IPAKeyboard(View):
    def get(self, request, *args, **kwargs):
        return render(request, "tools/ipa_keyboard.html")
