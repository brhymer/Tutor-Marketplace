from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),

  # === Student URLs
  # Student profile page
  path('students/<int:student_id>/', views.student_profile, name='student_profile'),

  # === Teacher URLs

  # === Lesson Booking URLs
  
  # === Language URLs
  path('languages/', views.language_index, name='language_index'),


  # === Auth URLs
  path('accounts/signup/', views.signup, name='signup'),

]