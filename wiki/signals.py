from django.core.mail import send_mail
from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.template.loader import render_to_string


@receiver(post_save, sender=ArticleHistory)
def send_article_wiki(sender, instance, created, **kwargs):
    if created:
        if instance.status != "2" and instance.status != "3":
            emails = User.objects.filter(groups__name="Wiki").exclude(is_active=False).exclude(is_staff=False).exclude(
                email="").values_list('email', flat=True)
            title = "New Wiki Suggesstion"
            message = render_to_string(
                'wiki/article_wiki_newsletter.html', {'change': instance, })
            for email in emails:
                send_mail(title, message, "forensicphonetician@gmail.com",
                          [email], fail_silently=True)
    else:
        if instance.status == "3":
            article = instance.article
            article.content = instance.newtext
            article.newsletter = False
            article.save()
        if instance.revert == True:
            article = instance.article
            article.content = instance.oldtext
            article.newsletter = False
            article.save()
