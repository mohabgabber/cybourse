from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from .serializer import *

# * Models imports
from articles.models import Article, Subject

# * Articles APIs


class ArticleListapi(APIView):
    def get(self, request, format=None):
        articles = Article.objects.all()
        serializer = ArticleMeta(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDetailapi(APIView):
    def get(self, request, pk, format=None):
        if Article.objects.filter(id=pk).exists():
            article = Article.objects.get(id=pk)
            serializer = ArticleSerializer(article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Article Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)


class SubjectListapi(APIView):
    def get(self, request, name, format=None):
        if Subject.objects.filter(name=name).exists():
            subj = Subject.objects.get(name=name)
            articles = Article.objects.filter(subject=subj)
            serializer = ArticleMeta(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'no such subject'}, status=status.HTTP_404_NOT_FOUND)
