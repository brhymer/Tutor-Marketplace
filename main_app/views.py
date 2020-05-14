from django.shortcuts import render, redirect
# TODO: change Subject to Language
from .models import Subject, Student, Teacher

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


# ==== STUDENT VIEWS


# ==== TEACHER VIEWS


# ==== LESSON VIEWS


# ==== LANGUAGE VIEWS
# Language Index View
def language_index(request):
    # get all languages from database
    # TODO: change Subject to Language
    languages = Subject.objects.all()
    template = 'languages/index.html'
    context = {
        'languages': languages,
    }
    # render template
    return render(request, template, context)