from django.contrib.admin.templatetags.admin_list import pagination
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from app.forms import LoginForm, SignupForm, AnswerForm
from app.models import Tag, Question, QuestionLike, Answer, AnswerLike
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib import auth

def pagination(objects_list, request, per_page=10):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_num)
    except InvalidPage:
        raise Http404("Страница не найдена")
    return page


def index(request):
    questions = Question.objects.get_newest()
    page = pagination(questions, request)
    return render(
        request, 'index.html',
        context={'questions': page.object_list, 'page_obj': page})


def question(request, question_id):
    question = Question.objects.prefetch_related('tags').get(id=question_id)
    likes = QuestionLike.objects.filter(question=question).count()
    answers = Answer.objects.annotate(num_likes=Count('a_likes')).filter(question_id=question_id)
    page = pagination(answers, request, 5)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
    return render(request, 'question.html', context={'question': question, 'answers': page.object_list, 'page_obj': page, 'q_likes': likes})


def hot(request):
    questions = Question.objects.get_hot()
    page = pagination(questions, request)
    return render(
        request, 'hot.html',
        context={'questions': page.object_list, 'page_obj': page})


def tag(request, tag_name):
    questions = Question.objects.get_by_tag(tag_name)
    page = pagination(questions, request, 5)
    return render(request, 'tag.html', context={'questions': page.object_list, 'tag_name': tag_name, 'page_obj': page})


@login_required
def edit(request):
    return render(request, 'edit.html')


def ask(request):
    return render(request, 'ask.html')


def login(request):
    form = LoginForm
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            form.add_error('password', 'Invalid username or password')
    return render(request, 'login.html', {"form": form})


def signup(request):
    form = SignupForm
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    return render(request, 'signup.html', {"form": form})

def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))
