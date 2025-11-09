from django.contrib import admin
from .models import Book

# Custom admin configuration for the Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns displayed in the list view
    list_display = ('title', 'author', 'publication_year')

    # Add filtering options on the sidebar
    list_filter = ('author', 'publication_year')

    # Add search functionality for title and author fields
    search_fields = ('title', 'author')

    # Optional: control how many books show per page
    list_per_page = 20
