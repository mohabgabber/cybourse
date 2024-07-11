from statistics import mode
from django.db import models
import uuid
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from questions.models import Question


class Subject(models.Model):
    id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=300)
    content = HTMLField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500)
    image = models.ImageField(
        upload_to='uploads/%Y/%m/%d/', default="uploads/default.jpg")
    newsletter = models.BooleanField(default=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE)
    keywords = models.CharField(
        max_length=1000, default="forensic phonetics & linguistics, forensic phonetics, phonetics")
    lastmodified = models.DateTimeField(auto_now=True)
    pdf = models.FileField(upload_to="articles/pdfs/%Y/%m/%d/",
                           validators=[FileExtensionValidator(["pdf"], "Wrong extension")], blank=True)
    quiz = models.ManyToManyField(Question, blank=True)
    total_xp = models.BigIntegerField(default=0)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"pk": str(self.id)})


class Featured(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]


class HomeText(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]


class Saved(models.Model):
    id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="saved")
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return self.owner.username


class ArticleView(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    score = models.BigIntegerField(default=0)
    percent = models.IntegerField(default=0)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"{self.user.username} viewed {self.article.title} at {self.date}"


class ProposedArticles(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    content = HTMLField()
    image = models.ImageField(
        upload_to="articles/suggestions/uploads/%Y/%m/%d/", default='uploads/default.jpg')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    actions = models.CharField(
        choices=(("1", "Accept"), ("2", "Deny"), ("3", "Pending")), max_length=100, default="3")

    def __str__(self):
        return f"{self.author.username} proposed {self.title}"
