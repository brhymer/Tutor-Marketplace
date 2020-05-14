from django.shortcuts import render, redirect
from .models import Language, Student, Teacher

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
    pass

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