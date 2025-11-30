from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all Book instances.
    
    Provides read-only access to all books in the database.
    Accessible to both authenticated and unauthenticated users.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public access
    
    # Add filtering and search functionality
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering

class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single Book instance by ID.
    
    Provides read-only access to a specific book's details.
    Accessible to both authenticated and unauthenticated users.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public access

class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new Book instance.
    
    Handles POST requests to create new books with data validation.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Using the specific import

    def perform_create(self, serializer):
        """
        Custom method called when creating a new book instance.
        Can be extended to add additional logic during creation.
        """
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing Book instance.
    
    Handles PUT and PATCH requests to update book details.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Using the specific import

    def perform_update(self, serializer):
        """
        Custom method called when updating a book instance.
        Can be extended to add additional logic during update.
        """
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a Book instance.
    
    Handles DELETE requests to remove books from the database.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Using the specific import

    def perform_destroy(self, instance):
        """
        Custom method called when deleting a book instance.
        Can be extended to add additional logic during deletion.
        """
        instance.delete()

# Optional: Author views for completeness
class AuthorListView(generics.ListAPIView):
    """
    ListView for retrieving all Author instances with their books.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single Author instance by ID.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]