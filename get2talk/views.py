from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from .forms import StudentForm
from .models import Teacher, Student, Lesson
from fpdf import FPDF
import os


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
        return JsonResponse({"success": False, "message": "There was an error."})


def get_dates_and_duration(request, teacher=None, month=None, year=None):
    lessons = Lesson.objects.filter(teacher=teacher, date__month=month, date__year=year)
    total_duration = list(lessons.values_list("duration"))
    total_duration_converted = [duration[0] for duration in total_duration]
    total_duration_converted = sum(total_duration_converted) / 60
    dates = lessons.dates("date", "day", "ASC")
    dates = list(dates)
    durations_by_days = {}
    for date in dates:
        durations = list(
            Lesson.objects.filter(teacher=teacher, date=date).values_list("duration")
        )
        total_duration_daily = sum([duration[0] for duration in durations])
        if date not in durations_by_days:
            durations_by_days[date] = 0
        durations_by_days[date] += total_duration_daily
    context = {
        "durations_by_days": durations_by_days,
        "total_duration": total_duration_converted,
    }
    return context


@login_required
def report_view(request):
    teacher = Teacher.objects.get(user=request.user)
    month = request.GET.get("month")
    year = request.GET.get("year")
    context = get_dates_and_duration(request, teacher=teacher, month=month, year=year)
    return render(request, "reports.html", context)


@login_required
def generate_pdf(request):
    month = request.GET.get("month")
    year = request.GET.get("year")
    teacher = Teacher.objects.get(user=request.user)
    context = get_dates_and_duration(request, teacher=teacher, month=month, year=year)

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    pdf.add_font(
        "DejaVu", "", R"dejavu-fonts-ttf-2.37\ttf\DejaVuSans-Bold.ttf", uni=True
    )
    pdf.set_font(family="Dejavu", size=24)
    pdf.cell(w=0, h=18, txt="Ewidencja czasu pracy", ln=1)
    pdf.set_font_size(14)
    pdf.cell(
        w=0,
        h=10,
        txt=f"Pracownik: {teacher.user.first_name} {teacher.user.last_name}",
        ln=1,
    )
    pdf.cell(w=0, h=10, txt=f"Miesiąc: {month}", ln=1)
    pdf.cell(w=0, h=10, txt="Firma: Get2Talk", ln=1)

    pdf.ln(10)

    pdf.set_font(family="Times", size=12, style="B")
    pdf.cell(w=50, h=10, txt="Data", border=1)
    pdf.cell(w=50, h=10, txt="Czas pracy", border=1, ln=1)

    pdf.set_font(family="Times", size=10)
    for date, duration in context["durations_by_days"].items():
        pdf.cell(w=50, h=5, txt=f"{date}", border=1)
        pdf.cell(w=50, h=5, txt=f"{duration} minut", border=1, ln=1)

    pdf.ln(10)

    pdf.set_font(family="Dejavu", size=18)
    pdf.cell(w=0, h=30, txt=f"Całkowity czas pracy: {context['total_duration']}")

    pdf.output("ewidencja.pdf")

    with open("ewidencja.pdf", "rb") as f:
        pdf_data = f.read()

    response = HttpResponse(pdf_data, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="ewidencja.pdf"'

    os.remove("ewidencja.pdf")
    return response
