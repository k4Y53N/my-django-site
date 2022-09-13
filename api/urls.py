from django.urls import path
from . import views

urlpatterns = [
    path('topics/', views.TopicListCreateView.as_view(), name='topic-list'),
    path('topics/<str:topic_name>/', views.ArticleListCreateView.as_view(), name='topic-detail'),
    path('articles/<int:pk>/', views.CommentListCreateView.as_view(), name='article-detail'),
]
