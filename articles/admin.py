from django.contrib import admin

from .models import *

admin.site.register(Article)
admin.site.register(Saved)
admin.site.register(Subject)
admin.site.register(Featured)
admin.site.register(HomeText)
admin.site.register(ArticleView)
admin.site.register(ProposedArticles)
admin.site.site_header = "FPHL Administration"
admin.site.site_title = "FPHL Administration Panel"
