from unicodedata import name
from django.db import models
import uuid
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    picture = models.ImageField(
        default="profile/default.jpg", upload_to="profile/pics/uploads/%Y/%m/%d")
    xp = models.BigIntegerField(default=0)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    date = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    bio = models.TextField(max_length=2000, blank=True)
    show_articles = models.BooleanField(default=True)
    show_quiz = models.BooleanField(default=True)
    # show_rank = models.BooleanField(default=True)
    rank = models.BigIntegerField(default=0)
    instagram = models.CharField(max_length=150, blank=True)
    twitter = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.picture.path)
        if img.height > img.width:
            # make square by cutting off equal amounts top and bottom
            left = 0
            right = img.width
            top = (img.height - img.width)/2
            bottom = (img.height + img.width)/2

            img = img.crop((left, top, right, bottom))  # type: ignore
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
        elif img.width > img.height:
            # make square by cutting off equal amounts left and right
            left = (img.width - img.height)/2
            right = (img.width + img.height)/2
            top = 0
            bottom = img.height
            img = img.crop((left, top, right, bottom))  # type: ignore
            # Resize the image to 300x300 resolution
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Point(models.Model):
    name = models.CharField(unique=True, max_length=100)
    amount = models.BigIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"In {self.name} we have {self.amount} XP"


class Rank(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="leaderboard")
    rank = models.BigIntegerField(default=0, unique=True)
    level = models.CharField(choices=(
        ("Phoenix", "Phoenix"), ("Unicorn", "Unicorn")), blank=True, null=True, max_length=100)

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return f"{self.profile.user} is {self.rank} on the website"
