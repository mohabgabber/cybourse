from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from articles.forms import CaptchaForm


# class Login(SuccessMessageMixin, LoginView):
#     template_name = "users/login.html"
#     success_message = "Successfully signed in 😎"
#     success_url = "home"

class Login(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, "You Are Already Registered 😺")
            return redirect("home")
        captcha = CaptchaForm()
        context = {"captcha": captcha}
        return render(request, "users/login.html", context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, "You Are Already Registered 😺")
            return redirect("home")
        captcha = CaptchaForm(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid() and captcha.is_valid():
            authing = authenticate(username=form.cleaned_data.get(
                "username"), password=form.cleaned_data.get("password"))
            if authing is not None:
                messages.success(request, "Successfully signed in 😎")
                login(request, authing)
                return redirect("home")
            else:
                messages.warning(request, "Wrong username or password 🫠")
        elif not form.is_valid():
            messages.warning(request, f"Error:{form.errors.as_text()}")
        else:
            messages.warning(request, f"{captcha.errors.as_text()}")

        context = {"captcha": captcha}
        return render(request, "users/login.html", context)


class Register(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, "You Are Already Registered 😺")
            return redirect("home")
        captcha = CaptchaForm()
        context = {"captcha": captcha}
        return render(request, "users/register.html", context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, "You Are Already Registered 😺")
            return redirect("home")
        form = SignupForm(request.POST)
        captcha = CaptchaForm(request.POST)
        if form.is_valid() and captcha.is_valid():
            new_user = User.objects.create_user(username=str(form.cleaned_data.get(
                "username")), password=form.cleaned_data.get("password"), email=form.cleaned_data.get("email"), first_name=form.cleaned_data.get("first_name"), last_name=form.cleaned_data.get("last_name"))
            login(request, new_user)
            messages.success(request, "Created your account successfully 😘")
            return redirect("home")
        elif not form.is_valid():
            messages.warning(request, f"Error: {form.errors.as_text()}")
        else:
            messages.warning(request, f"Error: {captcha.errors.as_text()}")
        context = {"captcha": captcha}
        return render(request, "users/register.html", context)


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.warning(request, "Logged Out Successfully")
        return redirect("home")


class ChangePassword(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        return render(request, "users/change-password.html", {"form": form, })

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Successfully Changed!")
            return redirect("home")
        else:
            messages.warning(request, "Error In Data Provided")
        return render(request, "users/change-password.html")


class DelAccountConf(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "users/delete-account-conf.html")


class DelAccount(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        messages.info(request, "Account Successfully Deleted 😭")
        return redirect("home")


# class UpdateEmail(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         return render(request, "users/update-email.html")

#     def post(self, request, *args, **kwargs):
#         form = UpdateEmail(request.POST)
#         if form.is_valid():
#         user = User.objects.get(username=request.user.username)
#         user.email = form.cleaned_data.get("email")
#         user.save()
#         else:
#             messages.warning(request, "Invalid")
#             return render(request, "users/update-email.html")
#         return redirect("home")
