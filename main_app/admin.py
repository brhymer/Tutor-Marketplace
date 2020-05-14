from django.contrib import admin
from .models import Teacher, Student, Language, Lesson

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Language)
admin.site.register(Lesson)