from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Language, Student, Teacher, Lesson
from .forms import LessonForm, TeacherForm

# Auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test


# User Permission Tests
def user_is_student(user):
    return user.student_set.count() != 0

def user_is_teacher(user):
    return user.teacher_set.count() != 0


# Home Views

def home(request):
    # get all languages from database
    languages = Language.objects.all()
    template = 'home.html'
    context = {
        'languages': languages,
    }
    return render(request, template, context)

def about(request):
    return render(request, 'about.html')


# ==== STUDENT VIEWS
# Student Private Profile
@login_required
@user_passes_test(user_is_student)
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
@login_required
@user_passes_test(user_is_teacher)
def teacher_profile(request, teacher_id):
    # get teacher from database by id
    teacher = Teacher.objects.get(id=teacher_id)
    # get lessons linked to teacher
    lessons = Lesson.objects.filter(teacher_id=teacher_id)
    unbooked_lessons = lessons.filter(student__isnull=True)
    # get unique students of teacher
    # find lessons with distinct students, returns list of lessons
    distinct_lessons = lessons.filter(student__isnull=False).distinct('student')
    students = []
    for lesson in distinct_lessons:
        # get student from lesson
        student = lesson.student_set.first()
        students.append(student)
    # if no students, returns students = [None]
    template = 'teachers/profile.html'
    context = {
        'teacher': teacher,
        'lessons': lessons,
        'students': students,
        'unbooked_lessons': unbooked_lessons,
    }
    return render(request, template, context)

# Teacher Public Profile
def teacher_details(request, teacher_id):
    # get teacher by id
    teacher = Teacher.objects.get(id=teacher_id)
    lessons = Lesson.objects.filter(teacher_id=teacher_id)
    # only show lessons that have not been booked by a student
    lessons_without_students = lessons.filter(student__isnull=True)
    template = 'teachers/details.html'
    context = {
        'teacher': teacher,
        'lessons': lessons_without_students,
    }
    return render(request, template, context)

# Edit Teacher Public Profile
@login_required
@user_passes_test(user_is_teacher)
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
    # only show lessons that have not been booked by a student
    lessons_without_students = lessons.filter(student__isnull=True)
    template = 'lessons/index.html'
    context = {
        'lessons': lessons_without_students,
        'language': language,
    }
    return render(request, template, context)

# NEW Lesson
@login_required
@user_passes_test(user_is_teacher)
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
                # save language to lesson
                lesson.language = teacher.language
                lesson.save()
            # redirect to teacher's profile
            return redirect('teacher_profile', teacher_id=teacher_id)
        else:
            form = LessonForm()
            template = 'lessons/new.html'
            context = { 'form': form }
            return render(request, template, context)
    else:
        # user is a student, doesn't have permissions
        student_id = user.student_set.first().id
        # give error message
        messages.error(request, 'Only teachers can make lessons')
        # redirect to student's profile page
        return redirect('student_profile', student_id=student_id)

# Delete Lesson
@login_required
@user_passes_test(user_is_teacher)
def delete_lesson(request, lesson_id):
    # TODO: only let teacher delete their own lesson
    # get lesson to delete from database
    lesson = Lesson.objects.get(id=lesson_id)
    # delete from database
    lesson.delete()
    # get teacher id from current user that's logged in
    user = request.user
    teacher_id = user.teacher_set.first().id
    # redirect to teacher's private profile
    return redirect('teacher_profile', teacher_id=teacher_id)


# Book a Lesson
def make_booking(request, lesson_id):
    # get the lesson from the database
    lesson = Lesson.objects.get(id=lesson_id)
    user = request.user
    # if user is registered and logged in
    if user.is_authenticated:
        # if user is not a student
        if user.student_set.count() == 0:
            # display an error message on the same page
            messages.error(request, 'Only students can book lessons')
            # redirect back to page that booking was initiated
            return redirect(request.META['HTTP_REFERER'])
        student = user.student_set.first()
        # add lesson to student's lessons
        student.lesson.add(lesson)
        # give confirmation message
        messages.success(request, 'Booking made!')
        # redirect to student's profile page
        return redirect('student_profile', student_id=student.id)
    # if user is not registered or logged in
    else:
        messages.error(request, 'Only registered users can book lessons. Please log in or sign up')
        return redirect('login')
    
# Cancel a Lesson
@login_required
def cancel_booking(request, lesson_id):
    # get lesson from database
    lesson = Lesson.objects.get(id=lesson_id)
    # get the student from the currently logged in user
    user = request.user
    student = user.student_set.first()
    # remove lesson from student's lesson, but don't delete lesson
    student.lesson.remove(lesson)
    # give confirmation message
    messages.success(request, 'Booking canceled')
    # redirect to student's profile
    return redirect('student_profile', student_id=student.id)
    # TODO: teacher's version of cancel? maybe?


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

def search(request):
    query = request.GET['query']
    # get all languages from database
    languages = Language.objects.filter(name__icontains=query)
    template = 'search.html'
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
            # redirect teachers to fill out their bio
            if user.teacher_set.count():
                return redirect('teacher_edit', user.teacher_set.first().id)
            else:
                return redirect('language_index')
        else:
            form = UserCreationForm()
            error_message = 'Error, Please Try Again'
            context = {
                'error': error_message,
                'form': form,
            }
            return render(request, 'registration/signup.html', context)
    else:
        form = UserCreationForm()
        context = {
            'error': error_message,
            'form': form,
        }
        return render(request, 'registration/signup.html', context)
