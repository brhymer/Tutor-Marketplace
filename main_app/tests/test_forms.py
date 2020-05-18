from django.test import TestCase

from main_app.forms import LessonForm, TeacherForm

class TeacherFormTest(TestCase):
    def test_teacher_form_full_name_field_label(self):
        form = TeacherForm()
        self.assertTrue(form.fields['full_name'].label == None or form.fields['full_name'].label == 'Full name')

    def test_teacher_form_language_field_label(self):
        form = TeacherForm()
        self.assertTrue(form.fields['language'].label == None or form.fields['language'].label == 'Language')

    def test_teacher_form_bio_field_label(self):
        form = TeacherForm()
        self.assertTrue(form.fields['bio'].label == None or form.fields['bio'].label == 'Bio')


class LessonFormTest(TestCase):
    def test_lesson_form_name_field_label(self):
        form = LessonForm()
        self.assertTrue(form.fields['name'].label == None or form.fields['name'].label == 'Name')

    def test_lesson_form_description_field_label(self):
        form = LessonForm()
        self.assertTrue(form.fields['description'].label == None or form.fields['description'].label == 'Description')

    def test_lesson_form_price_field_label(self):
        form = LessonForm()
        self.assertTrue(form.fields['price'].label == None or form.fields['price'].label == 'Price')

    def test_lesson_form_time_field_label(self):
        form = LessonForm()
        self.assertTrue(form.fields['time'].label == None or form.fields['time'].label == 'Time')

    def test_lesson_form_level_field_label(self):
        form = LessonForm()
        self.assertTrue(form.fields['level'].label == None or form.fields['level'].label == 'Level')
