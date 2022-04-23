from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from .forms import UserRegisterForm, UserLoginForm

class AuthenticationUser(CreateView):
    template_name = "accounts/user_auth.html"
    form_class = UserRegisterForm

    def get_context_data(self, **kwargs):
        context = super(AuthenticationUser, self).get_context_data(**kwargs)
        context["login_form"] = UserLoginForm()
        return context

class UserLoginView(LoginView):
    form_class = UserLoginForm

    def render_to_response(self, context, **response_kwargs):
        messages.error(self.request, "Error Authorisation !")
        print(self.get_form().errors)
        return redirect("user_auth")

    def get_success_url(self):
        messages.success(self.request, "Authorisation has been successfull !")
        print(self.get_form().errors)
        return reverse_lazy("home")


class UserRegisterView(CreateView):
    form_class = UserRegisterForm

    def render_to_response(self, context, **response_kwargs):
        messages.error(self.request, "Error Register !")
        return redirect("user_auth")

    def get_success_url(self):
        messages.success(self.request, "Registration has been successfull !")
        return reverse_lazy("home")

class ProfileView(DetailView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "profile"

def user_logout(request):
    messages.success(request, "You have been successfully logout")
    logout(request)
    return redirect("home")


