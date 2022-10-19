from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index,name="index"),
    path("internlogin/", views.internlogin,name="internlogin"),
    path("internsignup/", views.internsignup, name="internsignup"),
    path("handle_employee_signup/", views.handle_employee_signup,name="handle_employee_signup"),
    path("handle_employee_login/", views.handle_employee_login,name="handle_employee_login"),
    path("employeehome/", views.employeehome,name="employeehome"),
    path("managerhome/", views.managerhome,name="managerhome"),
    path("logout_view/", views.logout_view,name="logout_view"),
    path("employee_profile/", views.employee_profile,name="employee_profile"),
    path("make_comments/", views.make_comments,name="make_comments"),
    ]