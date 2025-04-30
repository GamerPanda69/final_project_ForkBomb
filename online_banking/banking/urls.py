# banking/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # The dashboard is now the root for the banking app ('/dashboard/')
    path('', views.dashboard, name='dashboard'),
    # These URLs handle the form submissions from the dashboard
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
]