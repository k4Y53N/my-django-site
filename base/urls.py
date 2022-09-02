from atexit import register
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('topics/<str:topic_name>/', views.topic_view, name='topic'),
    path('topics/<str:topic_name>/<int:article_id>', views.article_view, name='article'),
    path('add-msg/<comment_id>', views.add_comment_msg_view, name='add-msg')
    # path('add-topic/', views.add_topic_view, name='add-topic'),
]
