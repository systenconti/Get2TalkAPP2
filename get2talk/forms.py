from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("name", "mobile_number")

    def clean_name(self):
        name = self.cleaned_data["name"]
        return name.title()
