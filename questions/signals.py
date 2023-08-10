from unicodedata import name
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import QuestionLog, QuestionSet
from profiles.models import Point


@receiver(post_save, sender=QuestionLog)
def create_log(sender, instance, created, **kwargs):
    if created:
        if len(QuestionLog.objects.filter(user=instance.user, questionset=instance.questionset)) > 1:
            instance.delete()
        else:
            profile = instance.user.profile
            profile.xp += int((instance.percent/100) *
                              instance.questionset.total_xp)
            profile.save()


@receiver(post_save, sender=QuestionSet)
def add_points_to_total(sender, instance, created, **kwargs):
    if created:
        try:
            total = Point.objects.all()[0]
        except:
            total = Point.objects.create(name="Total points")
        total.amount += instance.total_xp
        total.save()
