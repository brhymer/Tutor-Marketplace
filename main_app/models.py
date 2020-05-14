from django.db import models
from django.contrib.auth.models import User

LEVEL = (
  ('B', 'Beginner'),
  ('I', 'Intermediate'),
  ('A', 'Advanced'),
)

# Data Models

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length =100)
    # Join table for what follows?
    # student = models.ManyToManyField(Student)
    # subject = models.ManyToManyField(Subject)
    # lesson = models.ManyToManyField(Lesson)
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
    # Join table to link to teacher/lesson?
    # teacher = models.ManyToManyField(Teacher)

    def __str__(self):
        return self.name


# Create Lesson as a join table?
# class Lesson(models.Model):
#     name = models.CharField(max_length =50)
#     teacher = models.ManyToManyField(Teacher)
#     student = models.ManyToManyField(Student)
#     subject = models.ManyToManyField(Subject)
#     description = models.TextField(max_length = 250)
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     time = models.DateTimeField()

#     def __str__(self):
#         return self.name


class Subject(models.Model):
    name = models.CharField(max_length =50)
    teachers = models.ManyToManyField(Teacher)

    def __str__(self):
        return self.name



