from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Question(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    quest = models.CharField(max_length=1000)
    opt1 = models.CharField(max_length=1000)
    opt2 = models.CharField(max_length=1000)
    opt3 = models.CharField(max_length=1000)
    opt4 = models.CharField(max_length=1000)
    ans = models.CharField(
        choices=(("1", "Opt1"), ("2", "Opt2"), ("3", "Opt3"), ("4", "Opt4"),), max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    video = models.FileField(validators=[FileExtensionValidator(
        ["mp4"], "Wrong Extension")], upload_to="questions/media/%Y/%m/%d/", null=True, blank=True)
    picture = models.FileField(validators=[FileExtensionValidator(
        ["png", "jpg", "jpeg"], "Wrong Extension")], upload_to="questions/media/%Y/%m/%d/", null=True, blank=True)
    audio = models.FileField(validators=[FileExtensionValidator(
        ["mp3"], "Wrong Extension")], upload_to="questions/media/%Y/%m/%d/", null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.quest


class QuizSubject(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class SubSubject(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class QuestionSet(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    questions = models.ManyToManyField(Question)
    name = models.CharField(max_length=1000, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(
        QuizSubject, on_delete=models.PROTECT, blank=True, null=True)
    subsubject = models.ForeignKey(
        SubSubject, on_delete=models.PROTECT, blank=True, null=True)
    solves = models.ManyToManyField(User, blank=True)
    private = models.BooleanField(default=False)
    choose_users = models.ManyToManyField(
        User, related_name="allowed_to_solve", blank=True)
    repeat_solves = models.BooleanField(default=True)
    hidden_answers = models.BooleanField(default=False)
    difficulty = models.CharField(
        choices=(("Easy", "Easy"), ("Intermediate", "Intermediate"), ("Hard", "Hard")), max_length=100)
    hide = models.BooleanField(default=False)
    total_xp = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name


class Score(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    questset = models.ForeignKey(
        QuestionSet, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} Got {self.score}"


class QuestionLog(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    questionset = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    percent = models.IntegerField(default=0)
    score = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} solved {self.questionset.name}"
