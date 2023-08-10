from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(QuestionSet)
admin.site.register(Score)
admin.site.register(QuestionLog)
admin.site.register(QuizSubject)
admin.site.register(SubSubject)
