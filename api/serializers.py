from rest_framework import serializers
from base.models import Topic, Article, Comment, Message
from django.contrib.auth.models import User


class UserSericlizers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'author_id']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_id']


class ArticleSerializers(serializers.ModelSerializer):
    # author = UserSericlizers(read_only=True)
    comment_set = CommentSerializer(many=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'comment_set']
        
    

class TopicSerializers(serializers.ModelSerializer):
    # article_set = ArticleSerializers(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'name', 'created', 'article_count']
