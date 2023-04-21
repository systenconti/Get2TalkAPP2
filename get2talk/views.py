from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print("Success")
            return redirect("dashboard")
        else:
            error_message = "Invalid login credentials"
            return render(request, "login.html", {"error_message": error_message})
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login_view")


@login_required()
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def add_new_student(request):
    return render(request, "new_student.html")


@login_required
def working_hours(request):
    return render(request, "working_hours.html")
