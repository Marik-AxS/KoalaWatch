from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logoutuser, name='logoutuser'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
]