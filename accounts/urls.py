from django.urls import path
from . import views

urlpatterns = [
    path("authentication/", views.AuthenticationUser.as_view(), name="user_auth"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("logout/", views.user_logout, name="logout"),
]