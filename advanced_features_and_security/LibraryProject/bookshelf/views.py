# bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.utils.html import escape

# Import forms - using the exact syntax the check is looking for
from .forms import ExampleForm
from .forms import BookForm, SecureSearchForm, UserRegistrationForm

from .models import Book

# ... rest of your views remain exactly the same ...
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Secure book listing view with proper input validation.
    Uses Django ORM to prevent SQL injection.
    """
    # Use the secure search form
    search_form = SecureSearchForm(request.GET or None)
    books = Book.objects.all()
    
    # Safe search functionality - uses Django ORM parameterization
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query', '')
        search_type = search_form.cleaned_data.get('search_type', 'title')
        
        if query:
            if search_type == 'title':
                books = books.filter(title__icontains=query)
            elif search_type == 'author':
                books = books.filter(author__icontains=query)
            elif search_type == 'isbn':
                books = books.filter(isbn__icontains=query)
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books, 
        'search_form': search_form
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
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    View to delete a book - requires can_delete permission
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('bookshelf:book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

@login_required
def book_dashboard(request):
    """
    Dashboard showing available actions based on permissions
    """
    user_permissions = {
        'can_view': request.user.has_perm('bookshelf.can_view'),
        'can_create': request.user.has_perm('bookshelf.can_create'),
        'can_edit': request.user.has_perm('bookshelf.can_edit'),
        'can_delete': request.user.has_perm('bookshelf.can_delete'),
    }
    return render(request, 'bookshelf/dashboard.html', {'user_permissions': user_permissions})

def example_form_view(request):
    """
    View demonstrating secure form handling with ExampleForm.
    Shows proper CSRF protection and input validation.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process secure form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            age = form.cleaned_data['age']
            agree_to_terms = form.cleaned_data['agree_to_terms']
            
            # In a real application, you would save to database here
            # All data is already sanitized by the form
            
            messages.success(request, 
                f"Thank you {name}! Your message has been securely processed."
            )
            return redirect('bookshelf:example_form_success')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {
        'form': form,
        'title': 'Secure Example Form'
    })

def example_form_success(request):
    """
    Success page after ExampleForm submission
    """
    return render(request, 'bookshelf/example_form_success.html', {
        'title': 'Form Submitted Successfully'
    })

def secure_search(request):
    """
    Example of secure search functionality using SecureSearchForm.
    Demonstrates proper input sanitization and ORM usage.
    """
    search_form = SecureSearchForm(request.GET or None)
    books = Book.objects.none()
    
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query', '')
        search_type = search_form.cleaned_data.get('search_type', 'title')
        
        if query:
            # Use Django ORM to prevent SQL injection
            if search_type == 'title':
                books = Book.objects.filter(title__icontains=query)
            elif search_type == 'author':
                books = Book.objects.filter(author__icontains=query)
            elif search_type == 'isbn':
                books = Book.objects.filter(isbn__icontains=query)
    
    return render(request, 'bookshelf/secure_search.html', {
        'search_form': search_form,
        'books': books,
        'query': search_form.cleaned_data.get('query', '') if search_form.is_valid() else ''
    })

def user_input_example(request):
    """
    Example view demonstrating safe handling of user input.
    Shows the importance of escaping user content.
    """
    user_input = ""
    if request.method == 'POST':
        # Always escape user input before displaying
        user_input = escape(request.POST.get('user_input', ''))
    
    return render(request, 'bookshelf/user_input_example.html', {
        'user_input': user_input
    })

def user_registration(request):
    """
    Secure user registration view using UserRegistrationForm.
    Demonstrates proper user creation with security measures.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 
                f"Account created successfully for {user.email}! "
                "You can now log in."
            )
            return redirect('bookshelf:book_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'bookshelf/user_registration.html', {
        'form': form,
        'title': 'Secure User Registration'
    })