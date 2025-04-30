# online_banking/online_banking/settings.py
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Generate a strong, unique key for production.
# For development, this is okay, but replace 'YOUR_SECRET_KEY_HERE'
SECRET_KEY = 'django-insecure-YOUR_SECRET_KEY_HERE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # Keep True for development, set to False for production

# ALLOWED_HOSTS is required when DEBUG is False.
# For development with DEBUG=True, it can often be empty.
# For production, list your domain names: ['yourdomain.com', 'www.yourdomain.com']
ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # <= REQUIRED FOR STATIC FILES

    # Your apps
    'authentication.apps.AuthenticationConfig',
    'banking.apps.BankingConfig',
    'financial_tools.apps.FinancialToolsConfig',
    'loan_estimation.apps.LoanEstimationConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Handles sessions
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', # Protects against CSRF attacks
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Associates users with requests using sessions
    'django.contrib.messages.middleware.MessageMiddleware', # Enables message framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'online_banking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Tell Django where to look for project-level templates (like base.html)
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True, # Allows Django to look inside app/templates/ directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # Adds request object to context
                'django.contrib.auth.context_processors.auth', # Adds user object to context
                'django.contrib.messages.context_processors.messages', # Adds messages to context
            ],
        },
    },
]

WSGI_APPLICATION = 'online_banking.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- Static files (CSS, JavaScript, Images) ---
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# URL to use when referring to static files located in STATIC_ROOT.
# Example: {% static 'css/style.css' %} -> /static/css/style.css
STATIC_URL = 'static/'

# Directories where Django will look for static files *in addition* to each app's 'static/' directory.
# This is where your project-wide static files (like your main style.css and script.js) should go.
STATICFILES_DIRS = [
    BASE_DIR / "static", # Looks for a 'static' folder in your project's root directory
]

# The absolute path to the directory where `collectstatic` will collect static files for deployment.
# This is NOT used by the development server (`runserver`). It's used when DEBUG=False.
# You typically don't need to configure this heavily for development unless using specific deployment tools.
# STATIC_ROOT = BASE_DIR / 'staticfiles_collected' # Example, often set in production settings

# --- End Static files ---


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Authentication Settings ---
LOGIN_REDIRECT_URL = 'dashboard' # URL name to redirect to after successful login
LOGOUT_REDIRECT_URL = 'login'    # URL name to redirect to after logout
LOGIN_URL = 'login'              # URL name of the login page itself
# --- End Authentication Settings ---