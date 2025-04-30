from django.urls import path
from .views import dashboard, deposit, withdraw

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('deposit/', deposit, name='deposit'),
    path('withdraw/', withdraw, name='withdraw'),
]