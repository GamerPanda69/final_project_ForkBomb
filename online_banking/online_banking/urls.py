from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm  # Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('register/', include('authentication.urls')),
    path('login/', LoginView.as_view(template_name='login.html', authentication_form=AuthenticationForm), name='login'),
    path('logout/', include('authentication.urls')),
    path('dashboard/', include('banking.urls')),
    path('tools/', include('financial_tools.urls')),
    path('loan/', include('loan_estimation.urls')),
]