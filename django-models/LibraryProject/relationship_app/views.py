from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .models import Library, Book, UserProfile, Author
from .forms import BookForm


# ... rest of your code remains the same ...

# Role check functions for user_passes_test
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role in ['Librarian', 'Admin']

def is_member(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role in ['Member', 'Librarian', 'Admin']

# Simple function-based view for listing books
def list_books(request):
    """Function-based view that lists all books"""
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Simple class-based view for library details
class LibraryDetailView(DetailView):
    """Class-based view that displays details for a specific library"""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Authentication views
def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Views with permission_required decorator (required by the check)
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """View to add a new book (requires can_add_book permission)"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('relationship_app:list_books')
    else:
        form = BookForm()
    
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    """View to edit an existing book (requires can_change_book permission)"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('relationship_app:list_books')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """View to delete a book (requires can_delete_book permission)"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('relationship_app:list_books')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})

# Role-based views using @user_passes_test decorator
@user_passes_test(is_admin, login_url='/relationship/login/')
def admin_view(request):
    """Admin dashboard - only accessible to Admin role"""
    users = UserProfile.objects.all().select_related('user')
    libraries = Library.objects.all()
    context = {
        'users': users,
        'libraries': libraries,
        'total_books': Book.objects.count(),
    }
    return render(request, 'relationship_app/admin_view.html', context)

@user_passes_test(is_librarian, login_url='/relationship/login/')
def librarian_view(request):
    """Librarian dashboard - accessible to Librarian and Admin roles"""
    libraries = Library.objects.all()
    books = Book.objects.all()
    context = {
        'libraries': libraries,
        'books': books,
        'available_books': books.count(),
    }
    return render(request, 'relationship_app/librarian_view.html', context)

@user_passes_test(is_member, login_url='/relationship/login/')
def member_view(request):
    """Member dashboard - accessible to all authenticated users with roles"""
    books = Book.objects.all()
    libraries = Library.objects.all()
    context = {
        'books': books,
        'libraries': libraries,
        'user_role': request.user.profile.role,
    }
    return render(request, 'relationship_app/member_view.html', context)