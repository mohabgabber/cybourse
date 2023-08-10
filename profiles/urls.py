from django.urls import path
from .views import *
urlpatterns = [
    path("profile/", ProfileDetail.as_view(), name="profile-detail"),
    path("@<str:username>/", PublicProfile.as_view(), name="profile-public"),
    path("@<str:username>/solved/", ProfileSolved.as_view(), name="profile-solved"),
    path("@<str:username>/contribs/",
         ProfileContributions.as_view(), name="profile-contribs"),
    path("leaderboard/", Leaderboard.as_view(), name="leaderboard"),
]
