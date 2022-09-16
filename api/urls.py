from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='api-home'),
    path('Topics/', views.TopicListCreateView.as_view(), name='topic-list'),
    path('Topics/<str:topic_name>/', views.TopicArticleListCreateView.as_view(), name='topic-detail'),
    path('Articles/', views.ArticleListView.as_view(), name='article-list'),
    path('Articles/<int:pk>/', views.ArticleCommentListCreateView.as_view(), name='article-detail'),
    path('Comments/', views.CommentListView.as_view(), name='comment-list'),
    path('Comments/<int:pk>/', views.CommentMessageListCreateView.as_view(), name='comment-detail'),
    path('Messages/', views.MessageListView.as_view(), name='message-list'),
    path('Messages/<int:pk>/', views.MessageRetrieveView.as_view(), name='message-detail'),
]
