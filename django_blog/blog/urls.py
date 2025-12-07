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
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    
    # DELETE - Remove post (Author only)
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # ========================================
    # Comment URLs
    # ========================================
    # CREATE - Add comment to post (Authenticated users)
    path('post/<int:pk>/comments/new/', views.add_comment, name='add_comment'),
    
    # UPDATE - Edit comment (Author only)
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_edit'),
    
    # DELETE - Remove comment (Author only)
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    
    # ========================================
    # Search and Tag URLs
    # ========================================
    # Search posts
    path('search/', views.search_posts, name='search_posts'),
    
    # Filter posts by tag (function-based, name parameter)
    path('tags/<str:tag_name>/', views.posts_by_tag, name='posts_by_tag'),
    
    # Filter posts by tag (class-based, slug parameter with django-taggit)
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts_by_tag_slug'),
    
    # Optional: Password reset URLs
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(template_name='blog/password_change.html'), 
         name='password_change'),
    path('password-change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='blog/password_change_done.html'), 
         name='password_change_done'),
]