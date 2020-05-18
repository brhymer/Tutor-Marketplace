from django.test import TestCase
from django.contrib.auth.models import User

from main_app.models import Student, Teacher, Lesson, Language


class StudentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up non-modified objects used by all test methods
        user = User.objects.create_user(username='test', password='test')
        user.student_set.create(full_name='Harry Potter')

    def test_full_name_label(self):
        student = Student.objects.get(id=1)
        field_label = student._meta.get_field('full_name').verbose_name
        self.assertEquals(field_label, 'full name')

    def test_object_name_is_full_name(self):
        student = Student.objects.get(id=1)
        expected_object_name = student.full_name
        self.assertEquals(expected_object_name, str(student))
