from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .forms import StudentForm
from .models import Teacher, Student


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
def working_hours_view(request):
    return render(request, "working_hours.html")
