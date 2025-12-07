# Django Blog Application

A full-featured blog application built with Django that allows users to create, read, update, and delete blog posts with authentication and authorization.

## Features

### 1. User Authentication
- User registration with email validation
- User login and logout
- User profile management
- Password change functionality

### 2. Blog Post Management (CRUD Operations)
Complete Create, Read, Update, and Delete functionality for blog posts with proper permissions and access control.

## Blog Post Features Documentation

### Overview
The blog post management system implements full CRUD (Create, Read, Update, Delete) operations using Django's class-based views with built-in permissions and security features.

---

## CRUD Operations Implementation

### 1. **CREATE - Creating New Posts**

**View Class:** `PostCreateView`
- **Base Class:** `LoginRequiredMixin, CreateView`
- **URL Pattern:** `/post/new/`
- **Template:** `blog/post_form.html`
- **Form:** `PostForm`
- **Permissions:** Only authenticated users can create posts

**Features:**
- Automatically sets the logged-in user as the post author
- Form validation ensures title is at least 5 characters
- Success message displayed after post creation
- Redirects to post list after successful creation

**Code Location:** `blog/views.py` (Lines 93-102)

```python
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)
```

**Usage:**
1. User must be logged in
2. Navigate to `/post/new/` or click "New Post" button
3. Fill in title and content
4. Click "Publish Post"

---

### 2. **READ - Viewing Posts**

#### a. List View - All Posts

**View Class:** `PostListView`
- **Base Class:** `ListView`
- **URL Pattern:** `/` (homepage)
- **Template:** `blog/post_list.html`
- **Permissions:** Public access (no authentication required)

**Features:**
- Displays all published posts in reverse chronological order
- Pagination (5 posts per page)
- Shows post excerpt (first 150 characters)
- Displays author and publication date
- Edit/Delete buttons visible only to post authors

**Code Location:** `blog/views.py` (Lines 79-86)

```python
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
```

#### b. Detail View - Individual Post

**View Class:** `PostDetailView`
- **Base Class:** `DetailView`
- **URL Pattern:** `/post/<int:pk>/`
- **Template:** `blog/post_detail.html`
- **Permissions:** Public access (no authentication required)

**Features:**
- Displays full post content
- Shows author information and timestamps
- Edit/Delete buttons visible only to post author
- "Back to Posts" navigation link

**Code Location:** `blog/views.py` (Lines 88-91)

```python
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
```

---

### 3. **UPDATE - Editing Posts**

**View Class:** `PostUpdateView`
- **Base Class:** `LoginRequiredMixin, UserPassesTestMixin, UpdateView`
- **URL Pattern:** `/post/<int:pk>/edit/`
- **Template:** `blog/post_form.html` (same as create)
- **Form:** `PostForm`
- **Permissions:** Only the post author can edit

**Features:**
- Pre-fills form with existing post data
- Form validation (same as create)
- Author-only access using `UserPassesTestMixin`
- Success message after update
- Redirects to post detail page after successful update

**Code Location:** `blog/views.py` (Lines 104-119)

```python
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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
```

**Usage:**
1. User must be logged in and be the post author
2. Click "Edit" button on post
3. Modify title or content
4. Click "Update Post"

**Security:**
- Non-authors attempting to access the edit URL will receive a 403 Forbidden error

---

### 4. **DELETE - Removing Posts**

**View Class:** `PostDeleteView`
- **Base Class:** `LoginRequiredMixin, UserPassesTestMixin, DeleteView`
- **URL Pattern:** `/post/<int:pk>/delete/`
- **Template:** `blog/post_confirm_delete.html`
- **Permissions:** Only the post author can delete

**Features:**
- Confirmation page before deletion
- Shows post preview
- Author-only access using `UserPassesTestMixin`
- Success message after deletion
- Redirects to post list after successful deletion

**Code Location:** `blog/views.py` (Lines 121-132)

```python
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)
```

**Usage:**
1. User must be logged in and be the post author
2. Click "Delete" button on post
3. Confirm deletion on confirmation page
4. Post is permanently removed

**Security:**
- Non-authors attempting to access the delete URL will receive a 403 Forbidden error

---

## Forms

### PostForm

**Location:** `blog/forms.py` (Lines 46-66)

**Fields:**
- `title` - CharField with TextInput widget
- `content` - TextField with Textarea widget

**Validation:**
- Title must be at least 5 characters long
- Both fields are required by default
- Custom styling with Bootstrap-compatible CSS classes

```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10
            }),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError("Title must be at least 5 characters long.")
        return title
```

---

## URL Configuration

**Location:** `blog/urls.py`

```python
urlpatterns = [
    # Read - List all posts
    path('', views.PostListView.as_view(), name='post_list'),
    
    # Read - View single post
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # Create - New post
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    
    # Update - Edit post
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    
    # Delete - Remove post
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
```

**URL Patterns:**
- `/` - Homepage with post list (public)
- `/post/new/` - Create new post (authenticated users only)
- `/post/<int:pk>/` - View individual post (public)
- `/post/<int:pk>/edit/` - Edit post (author only)
- `/post/<int:pk>/delete/` - Delete post (author only)

---

## Templates

### 1. post_list.html
Displays all blog posts in a grid layout with:
- Post title (clickable to detail view)
- Author and publication date
- Post excerpt
- Read More, Edit, and Delete buttons
- Pagination controls
- Empty state for when no posts exist

### 2. post_detail.html
Shows complete post with:
- Full post title and content
- Author information and timestamp
- Edit and Delete buttons (visible to author only)
- Navigation back to post list

### 3. post_form.html
Shared form for creating and editing posts with:
- Title input field
- Content textarea
- Submit button (context-aware: "Publish Post" or "Update Post")
- Cancel button
- Writing tips section
- Form validation error display

### 4. post_confirm_delete.html
Confirmation page for deletion with:
- Warning icon and message
- Post title display
- Post preview (first 50 words)
- Confirm and Cancel buttons

### 5. base.html
Base template with:
- Navigation bar with authentication-aware links
- Message display area
- Content block
- Footer
- Static file loading (CSS/JS)

---

## Permissions and Access Control

### Authentication Requirements

**Public Access (No Login Required):**
- View post list (`PostListView`)
- View individual posts (`PostDetailView`)

**Authenticated Users Only:**
- Create new posts (`PostCreateView`) - Uses `LoginRequiredMixin`

**Author-Only Access:**
- Edit posts (`PostUpdateView`) - Uses `LoginRequiredMixin` + `UserPassesTestMixin`
- Delete posts (`PostDeleteView`) - Uses `LoginRequiredMixin` + `UserPassesTestMixin`

### Security Implementation

**LoginRequiredMixin:**
- Redirects unauthenticated users to login page
- Applied to Create, Update, and Delete views

**UserPassesTestMixin:**
- Custom `test_func()` method checks if current user is the post author
- Returns 403 Forbidden if test fails
- Applied to Update and Delete views

```python
def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
```

---

## Data Handling

### Automatic Field Population

**Author Assignment:**
- Author is automatically set to the logged-in user in `form_valid()` method
- Users cannot manually set or change the author

**Timestamps:**
- `published_date` - Set to current time on creation
- `updated_date` - Automatically updated on each save (via `auto_now=True`)

### Data Validation

**Form Level:**
- Title minimum length: 5 characters
- Both title and content are required

**Model Level:**
- Title max length: 200 characters
- Content: TextField (unlimited length)
- Foreign key to User (author) with CASCADE deletion

---

## Testing Guidelines

### Manual Testing Checklist

**Create Functionality:**
- [ ] Unauthenticated user cannot access create page
- [ ] Authenticated user can create post with valid data
- [ ] Form validation prevents submission with title < 5 chars
- [ ] Success message appears after creation
- [ ] Author is correctly set to logged-in user
- [ ] Redirects to post list after creation

**Read Functionality:**
- [ ] Post list displays all posts
- [ ] Pagination works correctly (5 posts per page)
- [ ] Post detail shows complete content
- [ ] Public users can view posts without login

**Update Functionality:**
- [ ] Only post author can see Edit button
- [ ] Non-authors receive 403 error on direct URL access
- [ ] Form pre-fills with existing data
- [ ] Changes are saved correctly
- [ ] Success message appears after update
- [ ] Redirects to post detail after update

**Delete Functionality:**
- [ ] Only post author can see Delete button
- [ ] Non-authors receive 403 error on direct URL access
- [ ] Confirmation page displays before deletion
- [ ] Post is removed from database after confirmation
- [ ] Success message appears after deletion
- [ ] Redirects to post list after deletion

**Security Testing:**
- [ ] Direct URL manipulation blocked for non-authors
- [ ] CSRF protection enabled on all forms
- [ ] SQL injection prevention (Django ORM)
- [ ] XSS prevention (template auto-escaping)

---

## Installation and Setup

### Prerequisites
- Python 3.8+
- Django 5.2.8
- SQLite (included with Django)

### Installation Steps

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/django_blog
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install django
```

4. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser (optional):**
```bash
python manage.py createsuperuser
```

6. **Run development server:**
```bash
python manage.py runserver
```

7. **Access the application:**
- Open browser to `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`

---

## Usage Examples

### Creating a New Post

1. Register/Login to your account
2. Click "New Post" in navigation or go to `/post/new/`
3. Enter title: "My First Blog Post"
4. Enter content: "This is the content of my first blog post..."
5. Click "Publish Post"
6. Post appears in the list

### Editing a Post

1. Navigate to your post (you must be the author)
2. Click "Edit" button
3. Modify title or content
4. Click "Update Post"
5. Changes are saved and displayed

### Deleting a Post

1. Navigate to your post (you must be the author)
2. Click "Delete" button
3. Review the confirmation page
4. Click "Yes, Delete Post"
5. Post is removed and you're redirected to post list

---

## Project Structure

```
django_blog/
├── blog/
│   ├── migrations/
│   ├── static/
│   │   └── blog/
│   │       ├── css/
│   │       │   └── style.css
│   │       ├── js/
│   │       │   └── main.js
│   │       └── images/
│   ├── templates/
│   │   └── blog/
│   │       ├── base.html
│   │       ├── post_list.html
│   │       ├── post_detail.html
│   │       ├── post_form.html
│   │       ├── post_confirm_delete.html
│   │       ├── login.html
│   │       ├── register.html
│   │       └── profile.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── django_blog/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── README.md
```

---

## Key Files

### Models (`blog/models.py`)
- `Post` model with title, content, author, timestamps
- `UserProfile` model for extended user information

### Views (`blog/views.py`)
- Class-based views for CRUD operations
- Function-based views for authentication
- Permission mixins for security

### Forms (`blog/forms.py`)
- `PostForm` for creating/editing posts
- `CustomUserCreationForm` for registration
- `UserProfileForm` for profile management

### URLs (`blog/urls.py`)
- RESTful URL patterns for all operations
- Named URLs for easy referencing in templates

---

## Features Summary

✅ Complete CRUD operations for blog posts  
✅ User authentication (register, login, logout)  
✅ Permission-based access control  
✅ Author-only edit and delete  
✅ Form validation and error handling  
✅ Success messages for user feedback  
✅ Responsive design with CSS styling  
✅ Pagination for post lists  
✅ Public post viewing (no login required)  
✅ Secure against common vulnerabilities  

---

## Future Enhancements

- Comments system
- Categories and tags
- Search functionality
- Rich text editor (WYSIWYG)
- Image uploads for posts
- Social sharing buttons
- Draft/Publish status
- Post scheduling
- User follow system
- Email notifications

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## License

This project is part of the ALX Django Learning Lab curriculum.

---

## Support

For issues or questions:
- Create an issue on GitHub
- Contact: [Your contact information]

---

## Acknowledgments

- ALX Africa for the project requirements
- Django documentation
- Bootstrap for CSS framework inspiration

---

**Last Updated:** December 2025
**Version:** 1.0
**Author:** [Your Name]
