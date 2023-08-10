from django.urls import path
from .views import *

urlpatterns = [
    path("", QuestList.as_view(), name="questions-list"),
    path("detail/<str:pk>/", QuestionDetail.as_view(), name="questions-detail"),
    path("score/<str:pk>/", ScorePage.as_view(), name="score-page"),
    path("scores/list", ListScore.as_view(), name="scores-list")
]
