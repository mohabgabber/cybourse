from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from articles.models import ArticleView, Article
from questions.models import QuestionLog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ProfileDetail(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        context = {"profile": profile, }
        return render(request, "profiles/profile_detail.html", context)

    def post(self, request, *args, **kwargs):
        pform = ProfileForm(request.POST, request.FILES,
                            instance=request.user.profile)
        uform = UserForm(request.POST, instance=request.user)
        if pform.is_valid() and uform.is_valid():
            pform.save()
            uform.save()
            messages.success(request, "Successfully updated your profile")
            # return redirect("home")
        elif not uform.is_valid():
            messages.warning(request, f"{uform.errors.as_text()}")
        elif not pform.is_valid():
            messages.warning(request, f"{pform.errors.as_text()}")
        profile = Profile.objects.get(user=request.user)
        context = {"profile": profile, }
        return render(request, "profiles/profile_detail.html", context)


class PublicProfile(View):
    def get(self, request, username, *args, **kwargs):
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            articleviews = ArticleView.objects.filter(user=user)
            questionlog = QuestionLog.objects.filter(user=user)
            points = Point.objects.all()[0]
            # type: ignore
            if user.profile.xp >= points.amount:  # type: ignore
                rank = 1
            else:
                perc = (user.profile.xp/points.amount)*100  # type: ignore
                rank = int(100 - perc)
                if rank == 0:
                    rank += 1
            context = {"user": user, "profile": user.profile,  # type: ignore
                       "articles": articleviews, "questions": questionlog,  "rank": rank, }
        else:
            messages.warning(request, "User does not exist 🤧")
            return redirect("home")
        return render(request, "profiles/public_profile.html", context)


class ProfileSolved(View):
    def get(self, request, username, *args, **kwargs):
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            articleviews = ArticleView.objects.filter(user=user)
            questionlog = QuestionLog.objects.filter(user=user)
            points = Point.objects.all()[0]
            if user.profile.xp >= points.amount:  # type: ignore
                rank = 1
            else:
                perc = (user.profile.xp/points.amount)*100  # type: ignore
                rank = int(100 - perc)
                if rank == 0:
                    rank += 1
            context = {"user": user, "profile": user.profile,  # type: ignore
                       "articles": articleviews, "questions": questionlog,  "rank": rank, }
        else:
            messages.warning(request, "User does not exist 🤧")
            return redirect("home")
        return render(request, "profiles/profile_solved.html", context)


class ProfileContributions(View):
    def get(self, request, username, *args, **kwargs):
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            articleviews = ArticleView.objects.filter(user=user)
            questionlog = QuestionLog.objects.filter(user=user)
            contributions = Article.objects.filter(author=user)
            points = Point.objects.all()[0]
            if user.profile.xp >= points.amount:  # type: ignore
                rank = 1
            else:
                perc = (user.profile.xp/points.amount)*100  # type: ignore
                rank = int(100 - perc)
                if rank == 0:
                    rank += 1
            context = {"user": user, "profile": user.profile,  # type: ignore
                       "articles": articleviews, "questions": questionlog, "contribs": contributions, "rank": rank, }
        else:
            messages.warning(request, "User does not exist 🤧")
            return redirect("home")
        return render(request, "profiles/profile_contributions.html", context)


class Leaderboard(View):
    def get(self, request, *args, **kwargs):
        profiles = Profile.objects.all().order_by("-xp")
        p = Paginator(profiles, 15)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        page_obj = p.get_page(page_number)
        context = {"profiles": page_obj}
        return render(request, "profiles/leaderboard.html", context)
