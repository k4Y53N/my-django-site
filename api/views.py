from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from base.models import Topic, Article, Comment, Message
from . import serializers
from .permisions import IsOwnerOrReadOnly


class TopicListCreateView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = serializers.TopicSerializer

    def list(self, request, *args, **kwargs):
        queryset = Topic.objects.all()
        serializer = serializers.TopicSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def list(self, request, topic_name, *args, **kwargs):
        topic = get_object_or_404(Topic, name=topic_name)
        articles = Article.objects.filter(topic=topic)
        serializer = serializers.ArticleSerializer(
            articles,
            many=True,
            context={
                'request': request
            }
        )

        return Response(serializer.data)

    def create(self, request, topic_name, *args, **kwargs):
        topic = get_object_or_404(Topic, name=topic_name)
        serializer = serializers.ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(topic=topic, user=request.user)

        return Response(serializer.data)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def list(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        comments = Comment.objects.filter(article=article)
        serializer = serializers.CommentSerializer(comments, many=True)

        return Response(serializer.data)

    def create(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        serialzer = serializers.CommentSerializer(data=request.data)
        serialzer.is_valid(raise_exception=True)
        serialzer.save(article=article, user=request.user)

        return Response(serialzer.data)
