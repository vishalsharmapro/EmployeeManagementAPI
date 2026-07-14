from django.urls import path
from . import views

urlpatterns = [
    path("employees/", views.employee_list_api, name="employee_list_api"),
    path("employees/<int:id>/", views.employee_detail_api, name="employee_detail_api"),
]