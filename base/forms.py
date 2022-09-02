from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Article, Message, Topic, Comment


class LoginForm(ModelForm):
    class Meta:
        model = User
        field = ['username', 'email', 'password1', 'password2']
        exclude = []


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class TopicForm(ModelForm):
    def __init__(self, *args,  **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

    class Meta:
        model = Topic
        fields = '__all__'


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title']
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['content']