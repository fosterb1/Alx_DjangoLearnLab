# bookshelf/urls.py
from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('', views.book_dashboard, name='dashboard'),
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    # Security demonstration views
    path('example-form/', views.example_form_view, name='example_form'),
    path('example-form/success/', views.example_form_success, name='example_form_success'),
    path('secure-search/', views.secure_search, name='secure_search'),
    path('user-input-example/', views.user_input_example, name='user_input_example'),
    path('register/', views.user_registration, name='user_registration'),
]