from django.shortcuts import render
from django.core.paginator import Paginator

from app.models import *

# Create your views here.
QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'description': f'Lorem ipsum {i}'
    } for i in range(50)
]

ANSWERS = [
    {
        'id': i,
        'username': f'User that answered id {i}',
        'text': f'Lorem answer {i}'
    } for i in range(12)
]

USER = {
    'id': 1,
    'nickname': 'ukidoshi-nickname',
    'login': 'ukidoshi-login',
    'email': 'nsaryglar200@gmail.com',
}


def paginate(objects, page, per_page=5):
    paginator = Paginator(objects, per_page)
    return paginator.page(page)


def popular_tags_handler():
    tags = Tag.objects.get_popular_tags()
    return tags


def index(request):
    page = request.GET.get("page", 1)
    # questions = paginate(QUESTIONS, page)
    questions = paginate(Question.objects.find_new_questions(), page)
    return render(request, 'index.html',
                  {
                      'page_title': "Questions",
                      'items': questions,
                      'popular_tags': popular_tags_handler()
                  })


def hot_q(request):
    page = request.GET.get("page", 1)
    # questions = paginate(QUESTIONS, page)
    questions = paginate(Question.objects.find_hot_questions(), page)
    return render(request, 'index.html',
                  {
                      'page_title': "Questions",
                      'items': questions,
                      'hot': 1,
                      'popular_tags': popular_tags_handler()
                  })


def question(request, question_id):
    try:
        item = Question.objects.get(pk=question_id)
    except:
        return index(request)
    page = request.GET.get("page", 1)
    answers = Answer.objects.find_answers_to_question(item)
    answers = paginate(answers, page)
    question_info = answers.object_list[0].to_question
    return render(request, 'question.html',
                  {
                      'page_title': "Question",
                      'items': answers,
                      'question': question_info,
                      'popular_tags': popular_tags_handler()
                  })


def new_question(request):
    return render(request, 'new_question.html',
                  {
                      'page_title': "New question",
                      'popular_tags': popular_tags_handler()
                  })


def tag(request, tag_name):
    page = request.GET.get("page", 1)
    # questions = paginate(QUESTIONS, page)
    questions = paginate(Question.objects.find_with_tag(tag_name), page)
    return render(request, 'tag.html',
                  {
                      'page_title': f"Tag: {tag_name} | Questions",
                      'tag_name': tag_name,
                      'items': questions,
                      'popular_tags': popular_tags_handler()
                  })


def settings(request):
    return render(request, 'settings.html',
                  {
                      'page_title': "Settings",
                      "user": USER,
                      'popular_tags': popular_tags_handler()
                  })


def login(request):
    return render(request, 'login.html',
                  {
                      'page_title': "Login",
                      'popular_tags': popular_tags_handler()
                  })


def registration(request):
    return render(request, 'registration.html',
                  {
                      'page_title': "Register",
                      'popular_tags': popular_tags_handler()
                  })
