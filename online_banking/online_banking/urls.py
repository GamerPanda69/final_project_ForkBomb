# online_banking/online_banking/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings # Required for static files serving
from django.conf.urls.static import static # Required for static files serving

# A simple view to redirect the root URL based on authentication status
def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard') # Redirect logged-in users to the dashboard
    else:
        return redirect('login')     # Redirect anonymous users to the login page

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    # Group authentication related URLs under /auth/
    path('auth/', include('authentication.urls')),
    # Include banking URLs directly under /dashboard/ (as dashboard is its main page)
    path('dashboard/', include('banking.urls')),
    # Group financial tools URLs under /tools/
    path('tools/', include('financial_tools.urls')),
    # Group loan estimation URLs under /loan/
    path('loan/', include('loan_estimation.urls')),

    # Root URL redirection
    path('', root_redirect, name='root_redirect'),

    # Note: LoginView and LogoutView are handled within authentication.urls
]

# --- Static file serving configuration for Development ---
# This pattern tells Django's development server how to serve files found by STATICFILES_DIRS.
# It is ONLY active when DEBUG = True in settings.py.
# In production (DEBUG = False), a real web server like Nginx or Apache handles serving static files.
if settings.DEBUG:
    # The pattern uses STATIC_URL from settings ('static/')
    # and tells it to look for files in the directories specified by STATICFILES_DIRS
    # (in this case, the 'static' folder in the project root).
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")

    # If you were using STATIC_ROOT (for collectstatic), the line would be:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # But using STATICFILES_DIRS is more common and direct for development.
# --- End Static file serving configuration ---