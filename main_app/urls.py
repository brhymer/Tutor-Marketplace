from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),

  # === Student URLs
  # Student profile page
  path('students/<int:student_id>/', views.student_profile, name='student_profile'),

  # === Teacher URLs
  # Teachers index page, shows all teachers
  path('teachers/', views.teacher_index, name='teacher_index'),  

  # Teacher private profile page
  path('teachers/<int:teacher_id>/', views.teacher_profile, name='teacher_profile'),

  # Teacher public profile page
  path('teachers/<int:teacher_id>/details/', views.teacher_details, name='teacher_details'),

  # Edit Teacher public profile page
  path('teachers/<int:teacher_id>/edit/', views.teacher_edit, name='teacher_edit'),

  # Filter teachers by language
  path('languages/<int:language_id>/teachers/', views.teachers_filtered, name="teachers_filtered"),

  # === Lesson URLs
   # New Lesson
  path('lessons/new/', views.new_lesson, name='new_lesson'),

  # Delete Lesson
  path('lessons/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),

  # Book a Lesson
  path('lessons/<int:lesson_id>/book/', views.make_booking, name='make_booking'),

  # Cancel a Lesson Booking
  path('lessons/<int:lesson_id>/cancel/', views.cancel_booking, name='cancel_booking'),
  
  # Available lessons in the given language
  path('languages/<int:language_id>/lessons/', views.lesson_index, name="lesson_index"),

  # === Language URLs
  path('languages/', views.language_index, name='language_index'),
  path('search/', views.search, name ='search'),


  # === Auth URLs
  path('accounts/signup/', views.signup, name='signup'),

]