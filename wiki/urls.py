from django.urls import path
from .views import *

urlpatterns = [
    path("history/<str:pk>/", ListChanges.as_view(), name="changes-history"),
    path("edit/article/<str:pk>/", EditArticle.as_view(), name="change-edit"),
]
