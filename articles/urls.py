from django.urls import path
from .views import *
urlpatterns = [
    path("", ArticlesList.as_view(), name="home"),
    path("article/<str:pk>/", ArticleDetail.as_view(), name="article-detail"),
    path("save/<str:pk>/", SaveArticles.as_view(), name="save-article"),
    path("remove-save/<str:pk>/", RemoveSave.as_view(), name="remove-save"),
    path("account/", AccountPage.as_view(), name="account"),
    # path("about/", About.as_view(), name="about"),
    path("search/", Search.as_view(), name="search"),
    path("subject/<str:subject>/", Tag.as_view(), name="subject"),
    # path("contact/", Contact.as_view(), name="contact"),
    path("list/saved/articles/", ListSavedArticles.as_view(),
         name="saved-articles-list"),
    path("propose/", ProposeArticle.as_view(), name="propose-article"),
]
