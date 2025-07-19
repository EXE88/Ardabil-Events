from django.urls import path
from . import views

urlpatterns = [
    path("signup/",views.UserSignUp.as_view(),name="user_signup"),
]
