from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,CreateView,FormView
from .forms import RegistrationForm, LoginForm
from .models import User
from ..anime.models import Comment
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(CreateView):
    model = User
    template_name = 'pages/signup.html'
    form_class = RegistrationForm
    success_url = '/'


class LoginView(FormView):
    template_name = 'pages/login.html'
    form_class = LoginForm
    success_url = '/'
    model = User

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(self.request, 'Неправильный логин или пароль')
            return self.form_invalid(form)

        if user.check_password(password):
            if user.is_active:
                login(self.request, user)
                return redirect('index')
            else:
                messages.error(self.request, 'Пользователь забанен')
                return self.form_invalid(form)
        else:
            messages.error(self.request, 'Неправильный логин или пароль')
            return self.form_invalid(form)


def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

class ProfileView(TemplateView, LoginRequiredMixin):
    template_name = 'pages/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = kwargs.get('pk', self.request.user.id)
        user = User.objects.get(id=user_id)
        context['user'] = user
        context['favorite_anime'] = user.favorites.all()
        context['comments_user'] = Comment.objects.filter(author=user)
        return context

# Create your views here.
