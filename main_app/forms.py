from django import forms 
from .models import Lesson, Teacher


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'description', 'price', 'time', 'language', 'level']


class TeacherForm(forms.ModelForm):
    class Meta: 
        model = Teacher
        fields = ['full_name', 'language', 'lesson', 'bio']