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
    path("periodicreview/", views.periodicreview,name="periodicreview"),
    path("commentspage/<int:id>", views.commentspage,name="commentspage"),
    path("self_appraisal/", views.self_appraisal,name="self_appraisal"),
    path("self_appraisalpage/<int:id>", views.self_appraisalpage,name="self_appraisalpage"),
    path("self_appraisalform/", views.self_appraisalform,name="self_appraisalform"),
    path("make_appraisal/", views.make_appraisal,name="make_appraisal"),
    path("kpi/", views.kpi,name="kpi"),
    path("managersignup/", views.managersignup,name="managersignup"),
    path("managerlogin/", views.managerlogin,name="managerlogin"),
    path("handle_manager_login/", views.handle_manager_login,name="handle_manager_login"),
    path("handle_manager_signup/", views.handle_manager_signup,name="handle_manager_signup"),
    path("manager_profile/", views.manager_profile,name="manager_profile"),
    path("manager_kpi/", views.manager_kpi,name="manager_kpi"),
    path("manager_periodicreview/",views.manager_periodicreview,name="manager_periodicreview"),

    ]