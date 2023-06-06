from django import forms
from .models import Student, Suggestion


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("name", "mobile_number")

    def clean_name(self):
        name = self.cleaned_data["name"]
        return name.title()


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ("title", "description")
