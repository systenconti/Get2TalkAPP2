from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .forms import StudentForm
from .models import Teacher, Student, Lesson
from datetime import datetime


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            error_message = "Invalid login credentials"
            return render(request, "login.html", {"error_message": error_message})
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard_view(request):
    teacher = Teacher.objects.get(user=request.user)
    students = Student.objects.filter(teacher=teacher)
    context = {"teacher": teacher, "students": students}
    return render(request, "dashboard.html", context)


@method_decorator(login_required, name="dispatch")
class EditStudentView(View):
    template_name = "edit_student.html"

    def get(self, request, pk):
        student = Student.objects.get(id=pk)
        form = StudentForm(instance=student)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        student = Student.objects.get(id=pk)
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name="dispatch")
class AddNewStudentView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "new_student.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        form.instance.teacher = self.request.user.teacher
        return super().form_valid(form)


@login_required
def lessons_view(request):
    teacher = Teacher.objects.get(user=request.user)
    students = Student.objects.filter(teacher=teacher)
    lessons = Lesson.objects.filter(teacher=teacher)

    if request.method == "POST":
        student_id = request.POST.get("student")
        student = get_object_or_404(Student, pk=student_id, teacher=teacher)
        lesson_date = request.POST.get("lesson_date")
        duration = request.POST.get("duration")
        lesson = Lesson.objects.create(
            student=student, teacher=teacher, date=lesson_date, duration=duration
        )
        lesson.save()
        return redirect("lessons")

    context = {
        "teacher": teacher,
        "students": students,
        "lessons": lessons,
    }
    return render(request, "lesson_records.html", context)


@login_required
def delete_lesson(request, lesson_id):
    if request.method == "POST":
        lesson = get_object_or_404(Lesson, id=lesson_id)
        lesson.delete()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({'success': False, 'message': 'There was an error.'})
