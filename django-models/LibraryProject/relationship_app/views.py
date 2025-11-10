from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Book, Library, UserProfile

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