from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Student(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"


class Lesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    date = models.DateField()
    duration = models.PositiveIntegerField()

    def __str__(self):
        return f"Lesson with {self.student} {self.duration}"


class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=2000)
    date_submitted = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    supervisor_comment = models.CharField(max_length=3000, null=True)

    def __str__(self) -> str:
        return self.title
