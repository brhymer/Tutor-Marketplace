from django.shortcuts import render, redirect
from .models import Language, Student, Teacher, Lesson
from .forms import LessonForm, TeacherForm

# Auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def home(request):
    # get all languages from database
    languages = Language.objects.all()
    template = 'home.html'
    # define a range to loop over in the template
    # use to show 4 teachers in each language
    loop_range = range(0, 4)
    context = {
        'languages': languages,
        'range': loop_range,
    }
    return render(request, template, context)

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
    lessons = Lesson.objects.filter(teacher_id=teacher_id)
    template = 'teachers/profile.html'
    context = {
        'teacher': teacher,
        'lessons': lessons,
    }
    return render(request, template, context)

# Teacher Public Profile
def teacher_details(request, teacher_id):
    # get teacher by id
    teacher = Teacher.objects.get(id=teacher_id)
    lessons = Lesson.objects.filter(teacher_id=teacher_id)
    template = 'teachers/details.html'
    context = {
        'teacher': teacher,
        'lessons': lessons,
    }
    return render(request, template, context)

# Edit Teacher Public Profile
def teacher_edit(request, teacher_id):
    # get teacher from the database
    teacher = Teacher.objects.get(id=teacher_id)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        # update exisiting teacher
        if form.is_valid():
            teacher = form.save()
            return redirect('teacher_details', teacher_id=teacher.id)
    else:
        # send a form pre-populated with teacher's values
        form = TeacherForm(instance=teacher)
        template = 'teachers/edit.html'
        context = {
            'form': form,
            'teacher': teacher,
        }
        return render(request, template, context)


def teachers_filtered(request, language_id):
    # get all teachers for the given language
    teachers = Teacher.objects.filter(language_id=language_id)
    language = Language.objects.get(id=language_id)
    template = 'teachers/filtered.html'
    context = {
        'teachers': teachers,
        'language': language,
    }
    return render(request, template, context)


# ==== LESSON VIEWS
def lesson_index(request, language_id):
    # get all lessons in the given language
    language = Language.objects.get(id=language_id)
    lessons = Lesson.objects.filter(language_id=language_id)
    template = 'lessons/index.html'
    context = {
        'lessons': lessons,
        'language': language,
    }
    return render(request, template, context)

# NEW Lesson
def new_lesson(request):
    # get current logged in user
    user = request.user
    # check if user is a teacher
    if user.teacher_set.count() != 0:
        # get teacher id from current user
        teacher_id = user.teacher_set.first().id
        # get teacher from database
        teacher = Teacher.objects.get(id=teacher_id)
        if request.method == 'POST':
            form = LessonForm(request.POST)
            if form.is_valid():
                lesson = form.save()
                # save the teacher to newly made lesson
                lesson.teacher = teacher
                lesson.save()
            # redirect to teacher's profile
            return redirect('teacher_profile', teacher_id=teacher_id)
        else:
            form = LessonForm()
            template = 'lessons/new.html'
            context = { 'form': form }
            return render(request, template, context)
    else:
        # user is a teacher, doesn't have permissions
        student_id = user.student_set.first().id
        # redirect to student's profile page
        return redirect('student_profile', student_id=student_id)


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
            # get full name from form
            form_full_name = request.POST['full_name']
            if request.POST.get('student'):
                # create a Student instance
                user.student_set.create(full_name=form_full_name)
            elif request.POST.get('teacher'):
                # create a Teacher instance
                user.teacher_set.create(full_name=form_full_name)
            user.save()
            login(request, user)
            # TODO: redirect teachers to fill out their bio
            return redirect('language_index')
    else:
        form = UserCreationForm()
        context = {
            'error': error_message,
            'form': form,
        }
        return render(request, 'registration/signup.html', context)
