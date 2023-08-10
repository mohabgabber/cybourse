from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.template.loader import render_to_string
from questions.models import Score


class ArticlesList(View):
    def get(self, request, *args, **kwargs):
        Articles = Article.objects.all().order_by("-date")
        p = Paginator(Articles, 9)
        page_number = request.GET.get('page')
        featured = Featured.objects.all()[0]
        text = HomeText.objects.all()[0]
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        page_obj = p.get_page(page_number)
        if request.user.is_authenticated:
            context = {"articles": page_obj, "saved": Saved.objects.get(
                owner=request.user).articles.all(), "featured": featured, "text": text, }
        else:
            context = {"articles": page_obj,
                       "featured": featured, "text": text, }
        return render(request, "articles/home.html", context)


class ArticleDetail(View):
    def get(self, request, pk, *args, **kwargs):
        if Article.objects.filter(id=pk).exists():
            article = Article.objects.get(id=pk)
            if request.user.is_authenticated:
                context = {"article": article, "saved": Saved.objects.get(
                    owner=request.user).articles.all()}
                if ArticleView.objects.filter(article=article, user=request.user):
                    result = ArticleView.objects.get(
                        article=article, user=request.user)
                    context['result'] = result
            else:
                context = {"article": article, }
        else:
            messages.warning(request, "This Article Doesn't Exists")
            return redirect("home")
        return render(request, "articles/article-detail.html", context)

    def post(self, request, pk, *args, **kwargs):
        if Article.objects.filter(id=pk).exists():
            if request.user.is_authenticated:
                article = Article.objects.get(id=pk)
                if not ArticleView.objects.filter(article=article, user=request.user).exists():
                    # questions = article.quiz
                    score = 0
                    for q in article.quiz.all():
                        ans = request.POST.get(str(q.id))
                        if ans == q.ans:
                            score += 1
                    percent = int((score/article.quiz.count())*100)
                    if percent > 50:
                        result = ArticleView.objects.create(
                            user=request.user, article=article, score=score, percent=percent)
                        messages.success(
                            request, f"You passed 💃, you got {int((percent/100)*article.total_xp)} XP")
                        context = {"article": article, 'result': result, }
                    else:
                        messages.warning(
                            request, f"You did not pass 😥, you got {score} questions right")
                        context = {
                            "article": article, "msg": f"You did not pass, you got {score} questions right"}
                    return render(request, "articles/article-detail.html", context)
                else:
                    messages.warning(
                        request, "you already solved this article 😋")
                    return redirect("article-detail", article.id)
            else:
                messages.warning(request, "You need to login first")
                return redirect("article-detail", pk)
        else:
            messages.warning(request, "This Article Doesn't Exists")
            return redirect("home")


class SaveArticles(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        if Article.objects.filter(id=pk).exists():
            article = Article.objects.get(id=pk)
            if Saved.objects.filter(articles=article, owner=request.user).exists():
                messages.success(request, "This Article Is Already Saved")
            else:
                newsave = Saved.objects.get(owner=request.user)
                newsave.articles.add(article)
                messages.success(request, "Successfully Added Article!")
        else:
            messages.warning(request, "This Article Doesn't Exists")
        return redirect("home")


class RemoveSave(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        if Article.objects.filter(id=pk).exists():
            article = Article.objects.get(id=pk)
            if Saved.objects.filter(articles=article, owner=request.user).exists():
                newsave = Saved.objects.get(owner=request.user)
                newsave.articles.remove(article)
                messages.warning(request, "Successfully Removed Article!")
            else:
                messages.success(request, "This Article Wasn't Saved")
        else:
            messages.warning(request, "This Article Doesn't Exists")
        return redirect("home")


class Search(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        if query == '' or query == ' ':
            messages.warning(request, "you can't search everything human!")
            return redirect("home")
        articles = Article.objects.filter(Q(title__icontains=query))
        p = Paginator(articles, 6)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        page_obj = p.get_page(page_number)
        if request.user.is_authenticated:
            context = {'results': page_obj, "saved": Saved.objects.get(
                owner=request.user).articles.all()}
        else:
            context = {'results': page_obj, }
        return render(request, 'articles/search-results.html', context)


class AccountPage(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        savedarticles = Saved.objects.get(owner=request.user)
        context = {"saved": savedarticles.articles.all(), }
        return render(request, "articles/account.html", context)


class Tag(View):
    def get(self, request, subject, *args, **kwargs):
        if Subject.objects.filter(name=subject).exists():
            subj = Subject.objects.get(name=subject)
            articles = Article.objects.filter(
                subject=subj).order_by("-date")
            p = Paginator(articles, 6)
            page_number = request.GET.get('page')
            try:
                page_obj = p.get_page(page_number)
            except PageNotAnInteger:
                page_obj = p.page(1)
            except EmptyPage:
                page_obj = p.page(p.num_pages)
            page_obj = p.get_page(page_number)
            if request.user.is_authenticated:
                context = {"articles": page_obj, "tag": subj.name, "saved": Saved.objects.get(
                    owner=request.user).articles.all()}
            else:
                context = {"articles": page_obj, "tag": subj.name, }
        else:
            messages.warning(request, "Subject Does Not Exist")
            return redirect("home")
        return render(request, "articles/subject.html", context)


class ListSavedArticles(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        savedarts = Saved.objects.get(owner=request.user)
        return render(request, "articles/list-saved-arts.html", {"saved": savedarts.articles.all(), })


class ProposeArticle(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        subjects = Subject.objects.all()
        captchaform = CaptchaForm()
        context = {"subjects": subjects, 'captcha': captchaform, }
        return render(request, "articles/propose_article.html", context)

    def post(self, request, *args, **kwargs):
        captchaform = CaptchaForm(request.POST)
        form = ProposeForm(request.POST)
        if form.is_valid() and captchaform.is_valid():
            if Subject.objects.filter(name=form.cleaned_data.get("subject")).exists():
                ProposedArticles.objects.create(author=request.user, content=form.cleaned_data.get(
                    "content"), title=form.cleaned_data.get("title"), description=form.cleaned_data.get("description"), subject=Subject.objects.get(name=form.cleaned_data.get("subject")))
                messages.success(
                    request, "You have successfully proposed an article, we will review it shortly 😘")
                return redirect("home")
            else:
                messages.warning(request, "Subject doesn't exist")
        elif not form.is_valid():
            messages.warning(request, f"Error: {form.errors.as_text()}")
        else:
            messages.warning(request, f"Error: {captchaform.errors.as_text()}")
        subjects = Subject.objects.all()
        context = {"subjects": subjects, 'captcha': captchaform, }
        return render(request, "articles/propose_article.html", context)
