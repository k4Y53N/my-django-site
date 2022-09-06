from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_home_view),
    path('topics/', views.topic_list_create_view),
    path('topics/<str:topic_name>/', views.article_list_create_view),
    path('articles/<int:article_id>/', views.comment_list_create_view),
    path('comments/<int:comment_id>/', views.message_list_create_view),
]
