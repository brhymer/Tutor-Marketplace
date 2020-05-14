from django.shortcuts import render, redirect
from .models import Language, Student, Teacher

# Auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


# ==== STUDENT VIEWS
# Student Private Profile
def student_profile(request, student_id):
    # get student from database by id
    student = Student.objects.get(id=student_id)
    # define template to render
    template = 'students/profile.html'
    # define context to pass to template
    context = {
        'student': student,
    }
    return render(request, template, context)


# ==== TEACHER VIEWS


# ==== LESSON VIEWS


# ==== LANGUAGE VIEWS
# Language Index View
def language_index(request):
    # get all languages from database
    languages = Language.objects.all()
    template = 'languages/index.html'
    context = {
        'languages': languages,
    }
    # render template
    return render(request, template, context)



# ====AUTH VIEWS
# Signup
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('language_index')
    else:
        form = UserCreationForm()
        context = {
            'error': error_message,
            'form': form,
        }
        return render(request, 'registration/signup.html', context)
