from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.sitemaps.views import sitemap
from articles.sitemaps import ArticleSitemap
sitemaps = {
    "articles": ArticleSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),

    # * Apps
    path("", include("articles.urls")),
    path("auth/", include("users.urls")),
    path("questions/", include("questions.urls")),
    path("wiki/", include("wiki.urls")),
    path("api/", include("api.urls")),
    path("", include("profiles.urls")),

    # * SEO
    path("favicon.ico", RedirectView.as_view(
        url=staticfiles_storage.url("favicon.ico")),),
    path('robots.txt', TemplateView.as_view(
        template_name="articles/robots.txt", content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    # * Libraries and Frameworks
    path('tinymce/', include('tinymce.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
