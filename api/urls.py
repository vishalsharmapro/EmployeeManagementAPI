
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path(
        "employees/",
        views.EmployeeListCreateAPIView.as_view(),
        name="employee_list_api"
    ),

    path(
        "employees/<int:id>/",
        views.EmployeeRetrieveUpdateDestroyAPIView.as_view(),
        name="employee_detail_api"
    ),
 # JWT
    path( "token/",TokenObtainPairView.as_view(),name="token_obtain_pair" ),
    path("token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),

]
