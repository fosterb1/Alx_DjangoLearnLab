from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Library views (Class-based)
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Book views
    path('books/', views.list_books, name='list_books'),
    path('books/management/', views.book_management, name='book_management'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    
    # Authentication views
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.CustomLoginView.as_view(), name='login'),
    path('auth/logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Role-based dashboard views
    path('dashboard/admin/', views.admin_view, name='admin_view'),
    path('dashboard/librarian/', views.librarian_view, name='librarian_view'),
    path('dashboard/member/', views.member_view, name='member_view'),
]