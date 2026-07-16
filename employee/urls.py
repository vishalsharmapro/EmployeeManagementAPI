from django.urls import path

from . import views

urlpatterns=[

    path("employee/<int:id>/",views.single_employee),
    path("employee/",views.create_employee),
    path("employee/update/<int:id>/",views.update_employee),
    path("employee/delete/<int:id>/", views.delete_employee),
]