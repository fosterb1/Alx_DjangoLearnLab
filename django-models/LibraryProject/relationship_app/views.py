# relationship_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse
from .models import Book, Library, UserProfile, Author
from .forms import BookForm  # We'll create this form

# Role-based access control decorators (keep existing)
def admin_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, 'profile') and u.profile.role == 'Admin',
        login_url='/relationship/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def librarian_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, 'profile') and u.profile.role in ['Librarian', 'Admin'],
        login_url='/relationship/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def member_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, 'profile') and u.profile.role in ['Member', 'Librarian', 'Admin'],
        login_url='/relationship/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# Custom permission-protected views
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

# Book management dashboard (shows actions based on permissions)
@login_required
def book_management(request):
    """Book management dashboard showing available actions based on permissions"""
    books = Book.objects.all()
    user_permissions = {
        'can_add': request.user.has_perm('relationship_app.can_add_book'),
        'can_change': request.user.has_perm('relationship_app.can_change_book'),
        'can_delete': request.user.has_perm('relationship_app.can_delete_book'),
    }
    
    context = {
        'books': books,
        'user_permissions': user_permissions,
    }
    return render(request, 'relationship_app/book_management.html', context)

# Existing views (keep all previous views)
@login_required
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

class LibraryListView(ListView):
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'

class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Your role is: {user.profile.role}')
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

@admin_required
def admin_view(request):
    users = UserProfile.objects.all().select_related('user')
    libraries = Library.objects.all()
    context = {
        'users': users,
        'libraries': libraries,
        'total_books': Book.objects.count(),
    }
    return render(request, 'relationship_app/admin_view.html', context)

@librarian_required
def librarian_view(request):
    libraries = Library.objects.all()
    books = Book.objects.all()
    context = {
        'libraries': libraries,
        'books': books,
        'available_books': books.count(),
    }
    return render(request, 'relationship_app/librarian_view.html', context)

@member_required
def member_view(request):
    books = Book.objects.all()
    libraries = Library.objects.all()
    context = {
        'books': books,
        'libraries': libraries,
        'user_role': request.user.profile.role,
    }
    return render(request, 'relationship_app/member_view.html', context)