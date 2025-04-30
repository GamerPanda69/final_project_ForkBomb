from django.urls import path
from .views import tools

urlpatterns = [
    path('', tools, name='tools'),
]