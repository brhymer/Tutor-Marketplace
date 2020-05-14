from django.db import models
from django.contrib.auth.models import User



# Models

class Lesson(models.Model):
    name = models.CharField(max_length =50)
    # The below: ForeignKey or ManyToManyField?
    teacher = models.ManyToManyField(Teacher)
    student = models.ManyToManyField(Student)
    subject = models.ManyToManyField(Subject)
    description = models.TextField(max_length = 250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    time = models.DateTimeField()

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length =50)
    teacher = models.ForeignKey(Teacher)

    def __str__(self):
        


