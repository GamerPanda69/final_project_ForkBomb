from django.urls import path
from .views import loan_estimation

urlpatterns = [
    path('', loan_estimation, name='loan_estimation'),
]