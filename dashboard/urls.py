from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login"),
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/add/", views.add_employee, name="add_employee"),
    path("employees/edit/<int:id>/", views.edit_employee, name="edit_employee"),
    path("employees/delete/<int:id>/", views.delete_employee, name="delete_employee"),
    path("logout/", views.logout_user, name="logout"),
    path("employees/<int:id>/", views.employee_detail, name="employee_detail"),
    path("employees/pdf/", views.export_employee_pdf, name="export_employee_pdf"),
    path("employees/excel/",views.export_employee_excel, name="export_employee_excel"),
    path("reports/", views.reports, name="reports"),
    path("register/", views.register_page, name="register"),
    path("change-password/", views.change_password, name="change_password"),
]