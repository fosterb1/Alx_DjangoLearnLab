# blog/urls.py
"""
URL Configuration for Blog Application

This module defines all URL patterns for the blog app including:
- CRUD operations for blog posts (Create, Read, Update, Delete)
- User authentication (register, login, logout)
- User profile management
- Password change functionality

URL Pattern Structure:
    - Public URLs: Accessible to all users
    - Authenticated URLs: Require login
    - Author-only URLs: Require post ownership
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ========================================
    # READ Operations (Public Access)
    # ========================================
    # Home page - Post List
    path('', views.PostListView.as_view(), name='post_list'),
    
    # ========================================
    # Authentication URLs
    # ========================================
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # ========================================
    # Blog Post CRUD URLs
    # ========================================
    # READ - View individual post (Public)
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # CREATE - Create new post (Authenticated users)
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    
    # UPDATE - Edit post (Author only)
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    
    # DELETE - Remove post (Author only)
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Optional: Password reset URLs
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(template_name='blog/password_change.html'), 
         name='password_change'),
    path('password-change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='blog/password_change_done.html'), 
         name='password_change_done'),
]