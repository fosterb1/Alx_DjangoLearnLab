import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    Custom filter for Book model with advanced filtering options.
    
    Provides:
    - Case-insensitive title filtering
    - Range filtering for publication years
    - Multiple author filtering
    """
    title = django_filters.CharFilter(lookup_expr='icontains')
    publication_year__gt = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gt',
        label='Publication year greater than'
    )
    publication_year__lt = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lt',
        label='Publication year less than'
    )
    
    class Meta:
        model = Book
        fields = ['author', 'publication_year']