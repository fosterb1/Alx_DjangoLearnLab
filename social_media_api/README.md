# Social Media API

A comprehensive Django REST Framework-based social media API with complete social networking features including user authentication, follow system, posts, comments, likes, notifications, and personalized feed.

## Features

### ✅ User Authentication & Profile Management
- User registration with email validation
- Token-based authentication
- User profile management with bio and profile picture
- Follower/Following counts

### ✅ Social Connections
- Follow/Unfollow users
- View followers and following lists
- Automatic notifications for new followers

### ✅ Content Management
- Create, read, update, and delete posts
- Create, read, update, and delete comments
- Rich text content support
- Author-only edit permissions

### ✅ Engagement Features
- Like and unlike posts
- Like counts on posts
- Duplicate like prevention
- Automatic notifications for likes

### ✅ Personalized Feed
- View posts from followed users only
- Chronologically ordered feed
- Paginated results

### ✅ Notification System
- Real-time notifications for:
  - New followers
  - Post likes
  - Post comments
- Mark notifications as read
- Unread notification highlighting

### ✅ Advanced Features
- Pagination on all list endpoints
- Search and filtering capabilities
- Ordering options
- Token-based API authentication
- Comprehensive error handling

## Technology Stack

- **Backend Framework**: Django 5.2
- **API Framework**: Django REST Framework 3.14
- **Authentication**: Token Authentication
- **Database**: SQLite (Development) / PostgreSQL (Production recommended)
- **Filtering**: django-filter
- **Image Handling**: Pillow

## Project Structure

```
social_media_api/
├── accounts/               # User management & authentication
│   ├── models.py          # Custom User model with followers
│   ├── serializers.py     # User serializers
│   ├── views.py           # Auth & follow/unfollow views
│   └── urls.py            # Authentication & follow endpoints
├── posts/                 # Posts & comments management
│   ├── models.py          # Post, Comment, Like models
│   ├── serializers.py     # Post & comment serializers
│   ├── views.py           # CRUD views & feed
│   └── urls.py            # Posts, comments, feed endpoints
├── notifications/         # Notification system
│   ├── models.py          # Notification model
│   ├── serializers.py     # Notification serializers
│   ├── views.py           # Notification views
│   └── urls.py            # Notification endpoints
├── social_media_api/      # Project settings
│   ├── settings.py        # Configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI config
├── API_DOCUMENTATION.md   # Original API documentation
├── FEATURES_DOCUMENTATION.md  # Complete feature guide
├── DEPLOYMENT_GUIDE.md    # Production deployment guide
└── requirements.txt       # Python dependencies
```

## Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/social_media_api
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the API**
   - API Base URL: http://localhost:8000/api/
   - Admin Panel: http://localhost:8000/admin/
