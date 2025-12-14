#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    admin = User.objects.get(username='admin')
    admin.set_password('fqs+CpSwxKbTWDB-')
    admin.save()
    print("✅ Admin password changed successfully!")
except User.DoesNotExist:
    print("❌ Admin user not found")
