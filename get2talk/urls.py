from django.urls import path
from . import views
from .views import AddNewStudentView, EditStudentView

urlpatterns = [
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("add/", AddNewStudentView.as_view(), name="add_new_student"),
    path("edit/<int:pk>/", EditStudentView.as_view(), name="edit_student"),
    path("lessons/", views.lessons_view, name="lessons"),
]
