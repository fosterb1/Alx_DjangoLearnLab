# bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.utils.html import escape
from .models import Book
from .forms import BookForm

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Secure book listing view with proper input validation.
    Uses Django ORM to prevent SQL injection.
    """
    # Safe search functionality - uses Django ORM parameterization
    query = request.GET.get('q', '')
    if query:
        # Properly escaped and parameterized search
        safe_query = escape(query)
        books = Book.objects.filter(
            Q(title__icontains=safe_query) | 
            Q(author__icontains=safe_query) |
            Q(isbn__icontains=safe_query)
        )
    else:
        books = Book.objects.all()
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books, 
        'query': query
    })

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    Secure book creation view using Django forms for validation.
    CSRF protection is handled automatically by Django forms.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # Form validation prevents SQL injection and XSS
            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('bookshelf:book_list')
        else:
            # Form errors are safely handled
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form, 
        'action': 'Create'
    })

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    Secure book editing view with proper input validation.
    """
    # Safe object retrieval - prevents IDOR
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('bookshelf:book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form, 
        'action': 'Edit'
    })

@login_required
def safe_search(request):
    """
    Example of secure search functionality.
    Demonstrates proper input sanitization and ORM usage.
    """
    # Get and sanitize user input
    search_term = request.GET.get('search', '')
    sanitized_term = escape(search_term)
    
    # Use Django ORM to prevent SQL injection
    if sanitized_term:
        books = Book.objects.filter(
            title__icontains=sanitized_term
        )[:10]  # Limit results
    else:
        books = Book.objects.none()
    
    return render(request, 'bookshelf/search_results.html', {
        'books': books,
        'search_term': sanitized_term
    })

def user_input_example(request):
    """
    Example view demonstrating safe handling of user input.
    """
    user_input = ""
    if request.method == 'POST':
        # Always escape user input before displaying
        user_input = escape(request.POST.get('user_input', ''))
    
    return render(request, 'bookshelf/user_input_example.html', {
        'user_input': user_input
    })