from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login_view"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout_view"),
    path("add/", views.add_new_student, name="add_new_student"),
    path("hours/", views.working_hours, name="working_hours"),
]
