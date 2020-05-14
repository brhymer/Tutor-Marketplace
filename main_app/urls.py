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
  path('/teachers/', views.teacher_index, name='teacher_index'),  

  # Teacher private profile page
  path('teachers/<int:teacher_id>/', views.teacher_profile, name='teacher_profile'),

  # === Lesson Booking URLs
  
  # === Language URLs
  path('languages/', views.language_index, name='language_index'),


  # === Auth URLs
  path('accounts/signup/', views.signup, name='signup'),

]