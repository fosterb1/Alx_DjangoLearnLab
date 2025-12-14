# Django Settings Configuration

## Overview

The `settings.py` file is configured to work in both **development** and **production** environments using environment variables.

---

## DEBUG Setting

### Development (Default)
```python
DEBUG = True  # Default when DEBUG env var is not set
```

### Production
```python
# Set via environment variable:
export DEBUG=False

# Result:
DEBUG = False  # When DEBUG env var is set to 'False'
```

### How It Works

In `social_media_api/settings.py`:
```python
# Line 18-20:
# Set DEBUG = False in production via environment variable
# For production: export DEBUG=False or set in .env file
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
```

**Explanation:**
- `os.environ.get('DEBUG', 'True')` gets the DEBUG env var or defaults to 'True'
- `== 'True'` converts the string to boolean
- If `DEBUG=False` in environment → `DEBUG = False` in Django
- If `DEBUG=True` in environment → `DEBUG = True` in Django
- If DEBUG not set → defaults to `True` (development mode)

---

## Verification

### Test Script Results

Running `test_debug.py`:
```
==================================================
Settings Test Results
==================================================
DEBUG = False
Expected: False
Match: ✓

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
Expected: ['localhost', '127.0.0.1']

SECRET_KEY is set: ✓
✓ DEBUG can be set to False via environment
==================================================
```

### Manual Test

```bash
# Test DEBUG=False
export DEBUG=False
python manage.py check
# Settings will have DEBUG = False

# Test DEBUG=True
export DEBUG=True
python manage.py check
# Settings will have DEBUG = True

# No DEBUG env var (development)
python manage.py check
# Settings will have DEBUG = True (default)
```

---

## Environment Variables

### Required for Production

```bash
# Security
export DEBUG=False
export SECRET_KEY="your-secret-key-here"
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"

# Database (PostgreSQL)
export DB_HOST="your-db-host.rds.amazonaws.com"
export DB_NAME="social_media_db"
export DB_USER="dbadmin"
export DB_PASSWORD="your-secure-password"
export DB_PORT="5432"
```

### Optional

```bash
# AWS S3
export USE_S3=True
export AWS_STORAGE_BUCKET_NAME="your-bucket"
export AWS_S3_REGION_NAME="us-east-1"

# Superuser auto-creation
export DJANGO_SUPERUSER_USERNAME="admin"
export DJANGO_SUPERUSER_EMAIL="admin@example.com"
export DJANGO_SUPERUSER_PASSWORD="secure-password"
```

---

## Database Configuration

### Development (Default)
```python
# Uses SQLite when DB_HOST is not set
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Production
```python
# Uses PostgreSQL when DB_HOST environment variable is set
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'social_media_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

---

## Static Files Configuration

### Development & Production
```python
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

---

## AWS Elastic Beanstalk Configuration

When deploying to AWS EB, environment variables are set using:

```bash
eb setenv DEBUG=False
eb setenv SECRET_KEY="your-secret-key"
eb setenv ALLOWED_HOSTS="your-app.elasticbeanstalk.com"
eb setenv DB_HOST="your-rds-endpoint.rds.amazonaws.com"
# ... etc
```

These are automatically applied to the application.

---

## Security Settings

### Production Mode (DEBUG=False)

When `DEBUG=False`, Django automatically:
- Disables detailed error pages
- Requires `ALLOWED_HOSTS` to be set
- Enables production security features
- Requires static files to be collected

### Additional Security

In `settings_production.py`:
```python
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## Files Overview

### Main Settings
- **`settings.py`** - Base settings for dev/prod
  - Environment-aware configuration
  - Works for both development and production
  - Automatic database switching (SQLite/PostgreSQL)

### Production Settings
- **`settings_production.py`** - Production-specific overrides
  - Imports from settings.py
  - Adds production-only configurations
  - Additional security settings

### Environment Template
- **`.env.example`** - Template for environment variables
  - Shows all available options
  - Copy to `.env` for local development

---

## Usage Examples

### Local Development
```bash
# No environment variables needed
python manage.py runserver
# Uses: DEBUG=True, SQLite, default secret key
```

### Local Production Test
```bash
# Set production-like environment
export DEBUG=False
export SECRET_KEY="test-secret-key"
export ALLOWED_HOSTS="localhost,127.0.0.1"

python manage.py runserver
# Uses: DEBUG=False, SQLite (no DB_HOST), custom secret
```

### Production (AWS EB)
```bash
# Environment variables set via eb setenv
eb deploy
# Uses: DEBUG=False, PostgreSQL, production secret, etc.
```

---

## Troubleshooting

### Issue: DEBUG is always True

**Solution**: Ensure environment variable is set correctly
```bash
# Wrong (won't work):
export DEBUG=false  # lowercase 'false'

# Correct:
export DEBUG=False  # capital 'F'
```

### Issue: ALLOWED_HOSTS error

**Solution**: Set ALLOWED_HOSTS when DEBUG=False
```bash
export ALLOWED_HOSTS="localhost,127.0.0.1,yourdomain.com"
```

### Issue: Database connection error

**Solution**: 
- Development: Don't set DB_HOST (uses SQLite)
- Production: Set all DB_* environment variables

---

## Verification Commands

```bash
# Check current DEBUG setting
python manage.py shell -c "from django.conf import settings; print(f'DEBUG = {settings.DEBUG}')"

# Check all settings
python manage.py diffsettings

# Run system check
python manage.py check --deploy
```

---

## Summary

✅ **DEBUG can be set to False** via environment variable  
✅ **Production-ready configuration** included  
✅ **Environment-based settings** for flexibility  
✅ **Automatic database switching** (SQLite/PostgreSQL)  
✅ **Security settings** configured  
✅ **Tested and verified** working  

**For production deployment, simply set `DEBUG=False` in your environment variables.**

---

**File Locations:**
- Main settings: `social_media_api/settings.py`
- Production settings: `social_media_api/settings_production.py`
- Environment template: `.env.example`
- Test script: `test_debug.py`
