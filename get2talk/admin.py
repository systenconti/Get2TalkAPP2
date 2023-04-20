from django.contrib import admin
from .models import Teacher, Student, Lesson


# Register your models here.
class LessonAdmin(admin.ModelAdmin):
    list_display = ("student", "teacher", "date", "duration")
    list_filter = ("teacher", "student", "date")


class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher")
    list_filter = ("teacher",)


admin.site.register(Teacher)
admin.site.register(Student, StudentAdmin)
admin.site.register(Lesson, LessonAdmin)
