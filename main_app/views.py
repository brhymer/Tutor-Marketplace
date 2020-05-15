from django.shortcuts import render, redirect
from .models import Language, Student, Teacher, Lesson

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
# Teacher Index Page - show all teachers
def teacher_index(request):
    # get all teachers 
    teachers = Teacher.objects.all()
    template = 'teachers/index.html'
    context = {
        'teachers': teachers,
    }
    return render(request, template, context)

# Teacher Private Profile
def teacher_profile(request, teacher_id):
    # get teacher from database by id
    teacher = Teacher.objects.get(id=teacher_id)
    template = 'teachers/profile.html'
    context = {
        'teacher': teacher,
    }
    return render(request, template, context)


# ==== LESSON VIEWS
def lesson_index(request, language_id):
    # get all lessons in the given language
    lessons = Lesson.objects.filter(id=language_id)
    template = 'lessons/index.html'
    context = {
        'lessons': lessons,
    }
    return render(request, template, context)

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
