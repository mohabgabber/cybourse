from rest_framework import serializers
from articles.models import *


class ArticleSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name')
    author_name = serializers.CharField(source='author.username')

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'author_name', 'date',
                  'description', 'image', 'subject_name')


class ArticleMeta(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name')
    author_name = serializers.CharField(source='author.username')

    class Meta:
        model = Article
        fields = ('id', 'title', 'description', 'image',
                  'subject_name', 'author_name', 'date')


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
