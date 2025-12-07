# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, UserProfile, Comment, Tag
from .forms import CustomUserCreationForm, UserProfileForm, PostForm, CommentForm

# Authentication Views (keep these as function-based)
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Django Blog.')
            return redirect('post_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Welcome back, {username}!')
                return redirect('post_list')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'blog/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('post_list')

@login_required
def profile_view(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserProfileForm(instance=user)
    
    context = {
        'user_form': user_form,
        'profile': profile,
    }
    return render(request, 'blog/profile.html', context)

# ========================================
# Blog Post CRUD Views (Class-Based)
# ========================================
# These views implement complete Create, Read, Update, Delete operations
# for blog posts with appropriate permissions and access control.

class PostListView(ListView):
    """
    READ Operation - List all blog posts
    - Public access (no authentication required)
    - Displays posts in reverse chronological order
    - Implements pagination (5 posts per page)
    - Only shows posts with published_date <= current time
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    """
    READ Operation - Display individual blog post
    - Public access (no authentication required)
    - Shows complete post content with author info
    - Displays all comments
    - Comment form for authenticated users
    - Edit/Delete buttons visible only to post author
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    CREATE Operation - Create new blog post
    - Requires authentication (LoginRequiredMixin)
    - Automatically sets logged-in user as author
    - Uses PostForm for data validation
    - Redirects to post list after successful creation
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    UPDATE Operation - Edit existing blog post
    - Requires authentication (LoginRequiredMixin)
    - Author-only access (UserPassesTestMixin)
    - Pre-fills form with existing post data
    - Redirects to post detail after successful update
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    DELETE Operation - Remove blog post
    - Requires authentication (LoginRequiredMixin)
    - Author-only access (UserPassesTestMixin)
    - Shows confirmation page before deletion
    - Redirects to post list after successful deletion
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)

# ========================================
# Comment CRUD Views
# ========================================

@login_required
def add_comment(request, pk):
    """
    CREATE Operation - Add comment to blog post
    - Requires authentication
    - Creates comment linked to post and user
    """
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', pk=post.pk)
    
    return redirect('post_detail', pk=post.pk)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    UPDATE Operation - Edit existing comment
    - Requires authentication
    - Author-only access
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def form_valid(self, form):
        messages.success(self.request, 'Comment updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    DELETE Operation - Remove comment
    - Requires authentication
    - Author-only access
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)

# ========================================
# Search and Filter Views
# ========================================

def search_posts(request):
    """
    Search functionality for blog posts
    - Searches in title, content, and tags
    - Uses Q objects for complex queries
    """
    query = request.GET.get('q', '')
    posts = Post.objects.all()
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'blog/search_results.html', context)

def posts_by_tag(request, tag_name):
    """
    Filter posts by tag
    - Shows all posts with specified tag
    """
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.all()
    
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'blog/posts_by_tag.html', context)