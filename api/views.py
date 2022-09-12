from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .serializers import ArticleSerializers, CommentSerializer, MessageSerializer, TopicSerializers
from base.models import Article, Message, Topic, Comment


@api_view(['GET'])
def api_home_view(request):
    views = [
        'topics/',
        'topics/<str:topic_name>',
        'articles/<str:topic_name>',
        'comments/<int:comment_id>'
    ]

    return Response(views)


@api_view(['GET'])
def topic_list(request):
    topics = Topic.objects.all()
    serializers = TopicSerializers(topics, many=True)

    return Response(serializers.data)


class TopicListCreate(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializers


topic_list_create_view = TopicListCreate.as_view()


class TopicsRetrieve(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializers

    def retrieve(self, request, topic_name, *args, **kwargs):
        topic = Topic.objects.get(name=topic_name)
        serializer = TopicSerializers(topic)

        return Response(serializer.data)


topic_retrieve_view = TopicsRetrieve.as_view()


class ArticleListCreate(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializers

    def list(self, request, topic_name, *args, **kwargs):
        topic = get_object_or_404(Topic, name=topic_name)
        articles = self.queryset.filter(topic=topic)
        serializer = ArticleSerializers(articles, many=True)

        return Response(serializer.data)

    def create(self, request, topic_name, *args, **kwargs):
        topic = get_object_or_404(Topic, name=topic_name)
        data = request.data
        comments_data = data.pop('comment_set')
        article = Article.objects.create(
            author=request.user, topic=topic, **data)
        for comment_data in comments_data:
            comment = Comment.objects.create(
                article=article, author=request.user, **comment_data)
            comment.save()

        return Response(ArticleSerializers(article).data)


article_list_create_view = ArticleListCreate.as_view()


class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, article_id, *args, **kwargs):
        article = get_object_or_404(Article, pk=article_id)
        comments = Comment.objects.filter(article=article)
        serializers = CommentSerializer(comments, many=True)

        return Response(serializers.data)

    def create(self, request, article_id, *args, **kwargs):
        article = get_object_or_404(Article, pk=article_id)
        comment = Comment.objects.create(
            article=article, author=request.user, **request.data)
        comment.save()

        return Response(CommentSerializer(comment).data)


comment_list_create_view = CommentListCreate.as_view()


class MessageListCreate(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def list(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=comment_id)
        messages = Message.objects.filter(comment=comment)
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)

    def create(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=comment_id)
        message = Message.objects.create(
            author=request.user, comment=comment, **request.data)
        message.save()

        return Response(MessageSerializer(message).data)


message_list_create_view = MessageListCreate.as_view()
