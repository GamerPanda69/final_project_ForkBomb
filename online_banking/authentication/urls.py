# authentication/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    # Use LOGIN_URL and template_name from settings if possible, or specify here
    path('login/', LoginView.as_view(template_name='authentication/login.html'), name='login'),
    # Use LOGOUT_REDIRECT_URL from settings
    path('logout/', LogoutView.as_view(), name='logout'),
]