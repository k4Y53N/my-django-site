from http.client import IM_USED
from django.contrib import admin
from .models import Topic, Article, Comment, Message
# Register your models here.

admin.site.register(Topic)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Message)
