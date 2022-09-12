from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Topic, Article, Comment
from .forms import MessageForm, TopicForm, ArticleForm, CommentForm, UserCreationForm
# Create your views here.


def home_view(request: HttpRequest):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        topic_form = TopicForm(request.POST)
        if topic_form.is_valid():
            topic_form.save()

    topic_form = TopicForm()
    topic_form.fields['name'].required = False
    topics = Topic.objects.all()
    topic_name = request.GET.get('name')

    if bool(topic_name):
        topics = topics.filter(name__icontains=topic_name)

    context = {
        'topics': topics,
        'form': topic_form
    }
    return render(request, 'base/home.html', context)


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(request.META.get('HTTP_REFERER'))

    if request.method == 'GET':
        return render(request, 'base/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    if user is None:
        messages.error(request, 'login fail')
        return redirect('login')

    login(request, user)

    return redirect('home')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def register_view(request: HttpRequest):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'values are not valid')

    return render(request, 'base/register.html', {'form': form})


def topic_view(request: HttpRequest, topic_name):
    topic = get_object_or_404(Topic, name=topic_name)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        article_form = ArticleForm(request.POST)
        comment_form = CommentForm(request.POST)
        if article_form.is_valid() and comment_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.topic = topic
            article.save()

    article_form = ArticleForm()
    comment_form = CommentForm()
    articles = Article.objects.filter(topic=topic).order_by('-updated')
    title = request.GET.get('title')
    author = request.GET.get('author')

    if bool(title):
        articles = articles.filter(title__icontains=title)
    if bool(author):
        articles = articles.filter(author__username__icontains=author)

    context = {
        'topic': topic,
        'articles': articles,
        'article_form': article_form,
        'comment_form': comment_form
    }
    return render(request, 'base/topic.html', context)


def article_view(request: HttpRequest, topic_name, article_id):
    topic = get_object_or_404(Topic, name=topic_name)
    article = get_object_or_404(Article, pk=article_id)

    if article.topic.id != topic.id:
        return HttpResponseNotFound()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        comment_form = CommentForm(request.POST)
        if not comment_form.is_valid():
            messages.error(request, 'Cant add this invalid comment')
        else:
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
            article.save()

    comments = Comment.objects.filter(article=article)
    comment_form = CommentForm()
    message_form = MessageForm()

    context = {
        'topic': topic,
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'message_form': message_form,
    }
    return render(request, 'base/article.html', context)


@login_required(login_url='login')
def add_comment_msg_view(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    message_form = MessageForm(request.POST)
    if message_form.is_valid():
        message = message_form.save(commit=False)
        message.comment = comment
        message.user = request.user
        message.save()

    return redirect(request.META.get('HTTP_REFERER'), '/')
