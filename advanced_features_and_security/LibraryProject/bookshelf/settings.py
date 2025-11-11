# In settings.py
AUTH_USER_MODEL = 'bookshelf.CustomUser'

INSTALLED_APPS = [
    'bookshelf',  # Add this
    'relationship_app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]