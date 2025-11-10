# relationship_app/views.py
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .models import Book, Library, UserProfile

# Role-based access control decorators
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

# Role-based views
@admin_required
def admin_view(request):
    """Admin-only view for system administration"""
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
    """Librarian view for library management"""
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
    """Member view for library members"""
    books = Book.objects.all()
    libraries = Library.objects.all()
    context = {
        'books': books,
        'libraries': libraries,
        'user_role': request.user.profile.role,
    }
    return render(request, 'relationship_app/member_view.html', context)

# Update registration to set default role
def register(request):
    """User registration view with default Member role"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # UserProfile is automatically created by signal with default 'Member' role
            login(request, user)
            messages.success(request, f'Account created successfully! Your role is: {user.profile.role}')
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Existing views (keep these)
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