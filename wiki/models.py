from django.db import models
import uuid
from django.contrib.auth.models import User
from articles.models import Article
from tinymce.models import HTMLField


class ArticleHistory(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    oldtext = HTMLField(blank=False)
    newtext = HTMLField()
    status = models.CharField(
        choices=(("1", "Pending"), ("2", "Denied"), ("3", "Approved")), max_length=30, default="1")
    maker = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    changetext = models.CharField(max_length=500)
    revert = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.maker.username} Changed {self.article.title}"
