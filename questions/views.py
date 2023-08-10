from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class QuestList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        quests = QuestionSet.objects.all().order_by("-date")

        return render(request, "questions/list.html", {"questions": quests, })


@method_decorator(csrf_exempt, name='dispatch')
class QuestionDetail(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        if QuestionSet.objects.filter(id=pk).exists():
            qset = QuestionSet.objects.get(id=pk)
            if qset.hide:
                messages.warning(request, "Quiz does not exist")
                return redirect("questions-list")
            if qset.private:
                if request.user in qset.choose_users.all():
                    pass
                else:
                    messages.warning(request, "This Is A Private Exam")
                    return redirect("questions-list")
            else:
                pass
            if not qset.repeat_solves:
                if request.user in qset.solves.all():
                    messages.warning(
                        request, "This Is A One-Solve Only Exam, And You Did Solve It")
                    return redirect("questions-list")
                else:
                    pass
            else:
                pass
        else:
            messages.warning(request, "Question Set Doesn't Exist")
            return redirect("home")
        return render(request, "questions/quest-detail.html", {"questions": qset, })

    def post(self, request, pk, *args, **kwargs):
        if QuestionSet.objects.filter(id=pk).exists():
            qset = QuestionSet.objects.get(id=pk)
            if qset.private:
                if request.user in qset.choose_users.all():
                    pass
                else:
                    messages.warning(request, "This Is A Private Exam")
                    return redirect("questions-list")
            else:
                pass
            if not qset.repeat_solves:
                if request.user in qset.solves.all():
                    messages.warning(request, "This Is A One-Solve Only Exam")
                    return redirect("questions-list")
                else:
                    pass
            else:
                pass
            if qset.hide:
                messages.warning(request, "This quiz does not exist")
                return redirect("questions-list")
            score = 0
            for q in qset.questions.all():
                ans = request.POST.get(str(q.id))
                if ans == q.ans:
                    score += 1
            percent = int((score/qset.questions.count())*100)
            if percent > 50:
                if QuestionLog.objects.filter(user=request.user, questionset=qset).exists():
                    messages.success(
                        request, "You passed 🥳, but you did solve this before so no XP for you 😹")
                else:
                    QuestionLog.objects.create(
                        user=request.user, questionset=qset, score=score, percent=percent)
                    messages.success(
                        request, f"You passed 🤓, you got {int((percent/100)*qset.total_xp)} XP")
            else:
                messages.warning(request, "You didn't pass 🥺🥺🥺🥺")
            newscore = Score.objects.create(user=request.user, score=(
                score/qset.questions.count())*100, questset=qset)

            qset.solves.add(request.user)
            return redirect("score-page", newscore.id)
        else:
            messages.warning(request, "Question Set Doesn't Exist")
            return redirect("home")


class ScorePage(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        if Score.objects.filter(id=pk).exists():
            score = Score.objects.get(id=pk)
            # if QuestionSet.objects.filter(id=score.questset.id).exists():
            #     score = Score.objects.filter(
            #         user=request.user, questset=qset).latest("date")
            # else:
            #     messages.warning(
            #         request, "you haven't solved this question set yet")
            #     return redirect("questions-list")
        else:
            messages.warning(request, "this record does not exist")
            return redirect("questions-list")
        return render(request, "questions/score-page.html", {"quests": score})


class ListScore(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        userscores = Score.objects.filter(user=request.user).order_by("-date")
        return render(request, "questions/list-scores.html", {"scores": userscores, })
