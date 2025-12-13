# Social Media API - Deployment Guide

## Overview
This guide provides comprehensive instructions for deploying the Social Media API to production environments. We'll cover multiple hosting options and best practices.

---

## Pre-Deployment Checklist

### 1. Code Preparation

- [ ] All features tested locally
- [ ] Database migrations created and tested
- [ ] Static files configured
- [ ] Environment variables identified
- [ ] Security settings reviewed
- [ ] Dependencies documented in requirements.txt

### 2. Security Configuration

#### Update settings.py for Production

Create a production settings file or use environment variables:

**Option A: Create settings_production.py**
```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'your-app.herokuapp.com']

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database - Use environment variables
import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# Static Files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media Files (consider using AWS S3 for production)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# CORS (if frontend is on different domain)
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

**Option B: Use Environment Variables**
```python
import os
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

### 3. Create requirements.txt

```bash
cd C:\Users\foste\Alx_DjangoLearnLab\social_media_api
pip freeze > requirements.txt
```

Or manually create:
```txt
Django==5.2
djangorestframework==3.14.0
django-filter==23.5
Pillow==10.0.0
python-decouple==3.8
dj-database-url==2.1.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
whitenoise==6.6.0
```

### 4. Create .env.example

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@host:port/dbname
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

---

## Deployment Options

## Option 1: Heroku Deployment

### Step 1: Install Heroku CLI
Download and install from https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Prepare Project Files

**Create Procfile** (in project root):
```
web: gunicorn social_media_api.wsgi --log-file -
```

**Create runtime.txt** (specify Python version):
```
python-3.11.5
```

**Update requirements.txt**:
Add these if not present:
```
gunicorn
dj-database-url
psycopg2-binary
whitenoise
```

**Update settings.py**:
```python
# Add whitenoise to middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

# Static files with whitenoise
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Step 3: Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"

# Add PostgreSQL database
heroku addons:create heroku-postgresql:mini

# Deploy
git init  # if not already a git repo
git add .
git commit -m "Initial deployment"
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Collect static files
heroku run python manage.py collectstatic --noinput

# Open app
heroku open
```

### Step 4: Monitor Logs
```bash
heroku logs --tail
```

---

## Option 2: AWS Elastic Beanstalk

### Step 1: Install EB CLI
```bash
pip install awsebcli
```

### Step 2: Initialize EB Application

```bash
eb init -p python-3.11 social-media-api

# Select region and create SSH key
```

### Step 3: Create .ebextensions/django.config

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: social_media_api.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: social_media_api.settings
    PYTHONPATH: "/var/app/current:$PYTHONPATH"
  
container_commands:
  01_migrate:
    command: "source /var/app/venv/*/bin/activate && python manage.py migrate --noinput"
    leader_only: true
  02_collectstatic:
    command: "source /var/app/venv/*/bin/activate && python manage.py collectstatic --noinput"
    leader_only: true
```

### Step 4: Deploy

```bash
# Create environment
eb create social-media-api-env

# Set environment variables
eb setenv DEBUG=False SECRET_KEY="your-secret-key" ALLOWED_HOSTS="your-app.elasticbeanstalk.com"

# Deploy
eb deploy

# Open app
eb open
```

---

## Option 3: DigitalOcean App Platform

### Step 1: Create App

1. Go to DigitalOcean App Platform
2. Connect your GitHub repository
3. Configure build settings:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn --worker-tmp-dir /dev/shm social_media_api.wsgi`

### Step 2: Add Database

1. Add PostgreSQL database component
2. Note the connection string (DATABASE_URL will be auto-configured)

### Step 3: Configure Environment Variables

Add these in the App Platform dashboard:
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-app.ondigitalocean.app
```

### Step 4: Deploy

Click "Deploy" and monitor the build logs.

---

## Option 4: VPS Deployment (Ubuntu/Nginx/Gunicorn)

### Step 1: Server Setup

```bash
# Connect to your VPS
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y

# Create application user
adduser django
usermod -aG sudo django
su - django
```

### Step 2: Setup PostgreSQL

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE social_media_db;
CREATE USER social_media_user WITH PASSWORD 'your-password';
ALTER ROLE social_media_user SET client_encoding TO 'utf8';
ALTER ROLE social_media_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE social_media_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE social_media_db TO social_media_user;
\q
```

### Step 3: Deploy Application

```bash
# Clone repository
cd /home/django
git clone https://github.com/yourusername/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env file
nano .env
# Add your environment variables

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser
```

### Step 4: Configure Gunicorn

Create systemd service file:

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

```ini
[Unit]
Description=gunicorn daemon for social media api
After=network.target

[Service]
User=django
Group=www-data
WorkingDirectory=/home/django/Alx_DjangoLearnLab/social_media_api
EnvironmentFile=/home/django/Alx_DjangoLearnLab/social_media_api/.env
ExecStart=/home/django/Alx_DjangoLearnLab/social_media_api/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/home/django/Alx_DjangoLearnLab/social_media_api/gunicorn.sock \
          social_media_api.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

### Step 5: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/social_media_api
```

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/django/Alx_DjangoLearnLab/social_media_api;
    }
    
    location /media/ {
        root /home/django/Alx_DjangoLearnLab/social_media_api;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/django/Alx_DjangoLearnLab/social_media_api/gunicorn.sock;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/social_media_api /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

## Static Files Configuration

### Option A: WhiteNoise (Simple)

**settings.py:**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Option B: AWS S3 (Recommended for Production)

**Install:**
```bash
pip install boto3 django-storages
```

**settings.py:**
```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'storages',
]

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Static files
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

# Media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
```

---

## Database Migration

### PostgreSQL (Recommended for Production)

**settings.py:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

**Migrate from SQLite to PostgreSQL:**
```bash
# Backup SQLite data
python manage.py dumpdata > backup.json

# Configure PostgreSQL
# Update settings.py

# Create tables
python manage.py migrate

# Load data
python manage.py loaddata backup.json
```

---

## Monitoring and Maintenance

### Setup Logging

**settings.py:**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django_errors.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Monitoring Tools

1. **Sentry** - Error tracking
```bash
pip install sentry-sdk
```

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

2. **New Relic** - Performance monitoring
3. **Datadog** - Infrastructure monitoring

### Backup Strategy

**Automated Database Backups:**
```bash
# Create backup script
#!/bin/bash
BACKUP_DIR="/home/django/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U social_media_user -h localhost social_media_db > "$BACKUP_DIR/backup_$DATE.sql"

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

**Add to crontab:**
```bash
crontab -e
# Add: 0 2 * * * /home/django/backup.sh
```

---

## Post-Deployment Checklist

- [ ] SSL certificate installed and working
- [ ] Environment variables set correctly
- [ ] Database migrations applied
- [ ] Static files collected and serving correctly
- [ ] Media files configured
- [ ] Admin panel accessible
- [ ] API endpoints responding correctly
- [ ] Authentication working
- [ ] Notifications being created
- [ ] Feed displaying correctly
- [ ] Error logging configured
- [ ] Monitoring tools setup
- [ ] Backup strategy implemented
- [ ] DNS configured correctly
- [ ] CORS configured for frontend
- [ ] Rate limiting implemented
- [ ] Security headers enabled

---

## Maintenance Commands

```bash
# Check application logs
heroku logs --tail  # Heroku
sudo journalctl -u gunicorn -f  # VPS

# Run migrations
heroku run python manage.py migrate  # Heroku
python manage.py migrate  # VPS

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Database backup
python manage.py dumpdata > backup.json

# Database restore
python manage.py loaddata backup.json

# Clear sessions
python manage.py clearsessions
```

---

## Troubleshooting

### Static Files Not Loading
1. Check `STATIC_ROOT` and `STATIC_URL` settings
2. Run `python manage.py collectstatic`
3. Check Nginx/Apache configuration
4. Verify file permissions

### Database Connection Errors
1. Check `DATABASE_URL` environment variable
2. Verify database credentials
3. Ensure database server is running
4. Check firewall rules

### 502 Bad Gateway
1. Check Gunicorn is running: `sudo systemctl status gunicorn`
2. Check Nginx is running: `sudo systemctl status nginx`
3. Verify socket file permissions
4. Check application logs

### Import Errors
1. Ensure virtual environment is activated
2. Reinstall requirements: `pip install -r requirements.txt`
3. Check Python version compatibility

---

## Security Best Practices

1. **Never commit .env files or secrets**
2. **Use strong SECRET_KEY** (generate with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
3. **Keep dependencies updated**: `pip list --outdated`
4. **Enable HTTPS only** in production
5. **Implement rate limiting**: Consider django-ratelimit
6. **Regular security audits**: Use `python manage.py check --deploy`
7. **Monitor for vulnerabilities**: `pip install safety && safety check`

---

## Performance Optimization

1. **Database Indexing**: Add indexes to frequently queried fields
2. **Query Optimization**: Use `select_related()` and `prefetch_related()`
3. **Caching**: Implement Redis for caching
4. **CDN**: Use CloudFlare or AWS CloudFront
5. **Database Connection Pooling**: Configure `CONN_MAX_AGE`
6. **Compression**: Enable gzip compression in Nginx

---

## Support and Resources

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Heroku Django Guide: https://devcenter.heroku.com/articles/django-app-configuration
- DigitalOcean Tutorials: https://www.digitalocean.com/community/tags/django

---

## Deployment Verification

After deployment, verify these endpoints:

```bash
# Health check
curl https://your-domain.com/api/posts/

# Admin panel
https://your-domain.com/admin/

# API authentication
curl -X POST https://your-domain.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'
```

---

## Rollback Strategy

If deployment fails:

**Heroku:**
```bash
heroku releases
heroku rollback v123
```

**VPS:**
```bash
git checkout previous-commit-hash
sudo systemctl restart gunicorn
```

**Database:**
```bash
python manage.py loaddata backup.json
```

---

This deployment guide ensures your Social Media API is production-ready with proper security, monitoring, and maintenance procedures.
