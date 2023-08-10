from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Saved, Article, ArticleView, ProposedArticles
from profiles.models import Point


@receiver(post_save, sender=User)
def create_saved(sender, instance, created, **kwargs):
    if created:
        Saved.objects.create(owner=instance)


@receiver(post_save, sender=Article)
def create_newsletter(sender, instance, created, **kwargs):
    if created:
        try:
            total = Point.objects.all()[0]
        except:
            total = Point.objects.create(name="Total points")
        total.amount += instance.total_xp
        total.save()
    if instance.newsletter:
        subject = f'New Article 🥳🥳: {instance.title}'
        emails = User.objects.filter(is_active=True).exclude(
            email='').exclude(is_active=False).values_list('email', flat=True)
        message = render_to_string(
            'articles/article-newsletter.html', {'article': instance, })
        for email in emails:
            send_mail(subject, message, "forensicphonetician@gmail.com",
                      [email], fail_silently=True)
    else:
        pass


@receiver(post_save, sender=ArticleView)
def create_log(sender, instance, created, **kwargs):
    if created:
        if len(ArticleView.objects.filter(user=instance.user, article=instance.article)) > 1:
            instance.delete()
        else:
            profile = instance.user.profile
            profile.xp += int((instance.percent/100) *
                              instance.article.total_xp)
            profile.save()


@receiver(post_save, sender=ProposedArticles)
def article_suggestions(sender, instance, created, **kwargs):
    if instance.actions == "1":
        Article.objects.create(author=instance.author, content=instance.content,
                               image=instance.image, subject=instance.subject, description=instance.description, title=instance.title, newsletter=False,)
        profile = instance.author.profile
        profile.xp += 500
        profile.save()
        instance.delete()
    elif instance.actions == "2":
        instance.delete()
    else:
        pass
