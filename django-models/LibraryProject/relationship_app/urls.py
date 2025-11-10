from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Book and Library views (required by assignment)
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication views (required by assignment)
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]