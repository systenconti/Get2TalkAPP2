from django.contrib import admin
from .models import Teacher, Student, Lesson, Suggestion


class LessonAdmin(admin.ModelAdmin):
    list_display = ("student", "teacher", "date", "duration")
    list_filter = ("teacher", "student", "date")


class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher")
    list_filter = ("teacher",)


class SuggestionAdmin(admin.ModelAdmin):
    list_display = ("title", "user")
    list_filter = ("date_submitted", "user")


admin.site.register(Teacher)
admin.site.register(Student, StudentAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
