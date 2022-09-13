from urllib import request
from rest_framework import serializers
from base.models import Topic, Article, Comment, Message
from rest_framework.reverse import reverse


class MessageSerializer(serializers.ModelSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['username', 'content']

    def get_username(self, obj):
        return obj.user.username

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['title', 'content', 'created', 'updated', 'author', 'url']

    def get_author(self, obj):
        return obj.user.username

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        
        return reverse(
            viewname='article-detail',
            kwargs={
                'pk': obj.id,
            },
            request=request
        )
        

class TopicSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'name', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None

        return reverse('topic-detail', kwargs={'topic_name': obj.name}, request=request)
