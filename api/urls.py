from django.urls import path
from .views import *
urlpatterns = [

    # * Articles URLs

    path("articles/", ArticleListapi.as_view(), name="api-list-articles"),
    path("article/<str:pk>/", ArticleDetailapi.as_view(),
         name="api-detail-article"),
    path("subject/<str:name>/", SubjectListapi.as_view(), name="api-subject-list"),
]
