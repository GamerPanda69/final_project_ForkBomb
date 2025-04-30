# loan_estimation/urls.py
from django.urls import path
from . import views # Corrected import

urlpatterns = [
    path('', views.loan_estimation, name='loan_estimation'),
]