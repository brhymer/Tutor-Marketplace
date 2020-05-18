from django.db import models
from django.contrib.auth.models import User

LEVEL = (
  ('B', 'Beginner'),
  ('I', 'Intermediate'),
  ('A', 'Advanced'),
)

# Data Models


class Language(models.Model):
    name = models.CharField(max_length =50)
    
    def __str__(self):
        return self.name

    def get_lessons_without_students_count(self):
      return self.lesson_set.filter(student__isnull=True).count()



class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length =100)
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
    bio = models.TextField(null=True, max_length = 250)

    def __str__(self):
        return self.full_name


class Lesson(models.Model):
    name = models.CharField(max_length =50)
    description = models.TextField(max_length = 250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    time = models.DateTimeField()
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE)
    level = models.CharField(
    'Level',
    max_length=1,
    choices=LEVEL,
    default=LEVEL[0][0]
  )

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length =100)
    lesson = models.ManyToManyField(Lesson, null=True, blank=True)

    def __str__(self):
        return self.full_name







