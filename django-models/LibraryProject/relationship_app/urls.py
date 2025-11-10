# relationship_app/urls.py
from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    # Role-based views
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    
    # Book management with custom permissions
    path('books/manage/', views.book_management, name='book_management'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:pk>/', views.delete_book, name='delete_book'),
    
    # Protected views
    path('books/', views.list_books, name='list_books'),
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]