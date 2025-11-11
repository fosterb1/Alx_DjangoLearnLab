# LibraryProject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookshelf/', include('bookshelf.urls')),
    path('relationship/', include('relationship_app.urls')),
]