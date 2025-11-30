from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all Book instances with advanced query capabilities.
    
    Features Implemented:
    - Filtering: Filter books by author ID and publication year
    - Searching: Search across book titles and author names
    - Ordering: Order results by title, publication year, or author name
    
    Query Parameters Examples:
    - Filtering: /api/books/?author=1&publication_year=2020
    - Searching: /api/books/?search=harry
    - Ordering: /api/books/?ordering=title or /api/books/?ordering=-publication_year
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Filtering configuration
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Fields available for exact filtering
    filterset_fields = ['author', 'publication_year']
    
    # Fields available for text search
    search_fields = ['title', 'author__name']
    
    # Fields available for ordering
    ordering_fields = ['title', 'publication_year', 'author__name']
    
    # Default ordering if no ordering specified
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single Book instance by ID.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# Optional: Add filtering to Author views as well
class AuthorListView(generics.ListAPIView):
    """
    ListView for retrieving all Author instances with filtering and search capabilities.
    
    Query Parameters Examples:
    - Searching: /api/authors/?search=rowling
    - Ordering: /api/authors/?ordering=name
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single Author instance by ID.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]