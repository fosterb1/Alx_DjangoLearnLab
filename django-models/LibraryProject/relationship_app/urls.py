# relationship_app/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    # Protected views (require login)
    path('books/', views.list_books, name='list_books'),
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]