from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from base.models import Topic, Article, Comment, Message
from urllib.parse import unquote
from . import serializers
from .permisions import IsOwnerOrReadOnly


@api_view(['get'])
def home_view(request):
    return Response(
        [
            reverse(viewname='topic-list', request=request),
            reverse(viewname='article-list', request=request),
            reverse(viewname='comment-list', request=request),
            reverse(viewname='message-list', request=request),
        ]
    )


class TopicListCreateView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = serializers.TopicSerializer

    def list(self, request, *args, **kwargs):
        queryset = Topic.objects.all()
        serializer = serializers.TopicSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = [IsOwnerOrReadOnly]


class TopicArticleListCreateView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def list(self, request, topic_name, *args, **kwargs):
        topic = get_object_or_404(Topic, name=unquote(topic_name))
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
        serializer = serializers.ArticleSerializer(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(topic=topic, user=request.user)

        return Response(serializer.data)


class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]


class ArticleCommentListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def list(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        comments = Comment.objects.filter(article=article)
        serializer = serializers.CommentSerializer(
            comments,
            many=True,
            context={
                'request': request
            }
        )

        return Response(serializer.data)

    def create(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        serializer = serializers.CommentSerializer(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        article.save()
        serializer.save(article=article, user=request.user)

        return Response(serializer.data)


class MessageListView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = [IsOwnerOrReadOnly]


class CommentMessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def list(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        messgaes = Message.objects.filter(comment=comment)
        serializer = serializers.MessageSerializer(
            messgaes,
            many=True,
            context={
                'request': request
            }
        )

        return Response(serializer.data)

    def create(self, request, pk,  *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = serializers.MessageSerializer(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        comment.save()
        serializer.save(comment=comment, user=request.user)

        return Response(serializer.data)


class MessageRetrieveView(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, pk, *args, **kwargs):
        message = get_object_or_404(Message, pk=pk)
        serializer = serializers.MessageSerializer(
            message,
            context={
                'request': request
            }
        )

        return Response(serializer.data)
