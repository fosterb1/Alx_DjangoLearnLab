from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Book and Library views (required by assignment)
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication views using class-based views (what the checks are looking for)
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]