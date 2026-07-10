from django.urls import path


from . import views

urlpatterns=[
    path("test/",views.test),
    path("register/",views.register),
    path("login/", views.login),
]