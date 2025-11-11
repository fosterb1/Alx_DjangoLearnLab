"""
Django settings for LibraryProject project.
"""

import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.yourdomain.com']  # Add your production domain

# ============================================================================
# HTTPS AND SECURITY CONFIGURATIONS
# ============================================================================

# HTTPS REDIRECT SETTINGS
# ----------------------------------------------------------------------------
# SECURE_SSL_REDIRECT: Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = not DEBUG

# SECURE_PROXY_SSL_HEADER: Required when running behind a reverse proxy
# Tells Django to trust the X-Forwarded-Proto header from the proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HSTS (HTTP Strict Transport Security) SETTINGS
# ----------------------------------------------------------------------------
# SECURE_HSTS_SECONDS: Time browsers should remember to only use HTTPS
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0  # 1 year in production
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG

# SECURE COOKIE SETTINGS
# ----------------------------------------------------------------------------
# Secure cookies - only sent over HTTPS
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

# Additional cookie security
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # CSRF cookie needs JS access
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# SECURITY HEADERS CONFIGURATION
# ----------------------------------------------------------------------------
# Browser security headers
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# Referrer policy
SECURE_REFERRER_POLICY = 'same-origin'

# CSRF settings
CSRF_TRUSTED_ORIGINS = ['https://*.yourdomain.com']  # Add your production domain

# ============================================================================
# APPLICATION CONFIGURATION
# ============================================================================

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf',
    'relationship_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'LibraryProject.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# ============================================================================
# SECURITY DOCUMENTATION
# ============================================================================
"""
SECURITY CONFIGURATIONS IMPLEMENTED:

HTTPS AND SSL CONFIGURATION:
1. SECURE_SSL_REDIRECT: Redirects all HTTP traffic to HTTPS
2. SECURE_PROXY_SSL_HEADER: Configures proxy header trust for HTTPS detection
3. SECURE_HSTS_SECONDS: Enables HSTS with 1-year duration
4. SECURE_HSTS_INCLUDE_SUBDOMAINS: Applies HSTS to all subdomains
5. SECURE_HSTS_PRELOAD: Allows HSTS preloading in browsers

SECURE COOKIES:
6. CSRF_COOKIE_SECURE: CSRF cookies only sent over HTTPS
7. SESSION_COOKIE_SECURE: Session cookies only sent over HTTPS
8. SESSION_COOKIE_HTTPONLY: Prevents JavaScript access to session cookies
9. SAME_SITE_COOKIES: CSRF protection for same-site requests

SECURITY HEADERS:
10. SECURE_BROWSER_XSS_FILTER: Enables browser XSS filtering
11. X_FRAME_OPTIONS: Prevents clickjacking by denying framing
12. SECURE_CONTENT_TYPE_NOSNIFF: Prevents MIME type sniffing
13. SECURE_REFERRER_POLICY: Controls Referer header leakage

OTHER SECURITY:
14. DEBUG mode properly set for production/development
15. Strong password validation enforced
16. CSRF middleware enabled
17. Clickjacking protection middleware enabled
18. Custom CSP middleware for Content Security Policy
"""

# ============================================================================
# ENVIRONMENT-SPECIFIC SETTINGS
# ============================================================================

# Development-specific settings
if DEBUG:
    # Allow less restrictive settings for development
    ALLOWED_HOSTS = ['*']  # Allow all hosts in development
    SECURE_SSL_REDIRECT = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0