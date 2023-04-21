from django import forms
from .models import Student, Lesson


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("name", "mobile_number")
