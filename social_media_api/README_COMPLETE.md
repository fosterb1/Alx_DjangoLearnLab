# Social Media API - Complete Documentation

A comprehensive Django REST Framework-based social media API with complete social networking features.

## 📚 Documentation Index

- **[FEATURES_DOCUMENTATION.md](FEATURES_DOCUMENTATION.md)** - Complete API feature guide with examples
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Posts & comments API documentation
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Production deployment instructions
- **[POSTS_README.md](POSTS_README.md)** - Posts feature documentation

## ✨ All Features Implemented

### Task 2: User Follows and Feed ✅
- ✅ User model updated with `followers` field (many-to-many relationship)
- ✅ Follow/Unfollow API endpoints (`/api/auth/follow/<id>/`, `/api/auth/unfollow/<id>/`)
- ✅ Feed endpoint (`/api/feed/`) showing posts from followed users
- ✅ Proper permissions (users can only modify their own following list)
- ✅ Notifications created when someone follows you

### Task 3: Notifications and Likes ✅
- ✅ Like model created with unique constraint (user, post)
- ✅ Notification model with GenericForeignKey support
- ✅ Like/Unlike endpoints (`/api/posts/<id>/like/`, `/api/posts/<id>/unlike/`)
- ✅ Notification endpoints (`/api/notifications/`, `/api/notifications/<id>/read/`)
- ✅ Automatic notifications for:
  - New followers
  - Post likes
  - Post comments
- ✅ Duplicate like prevention
- ✅ Read/unread notification tracking

### Task 4: Deployment Ready ✅
- ✅ Production settings guide
- ✅ Multiple deployment options (Heroku, AWS, DigitalOcean, VPS)
- ✅ Security configurations
- ✅ Static files management (WhiteNoise & AWS S3)
- ✅ Database migration guide (SQLite to PostgreSQL)
- ✅ SSL setup instructions
- ✅ Monitoring and logging configuration
- ✅ Backup strategies

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/yourusername/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 2. Access Points
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Feed: http://localhost:8000/api/feed/
- Notifications: http://localhost:8000/api/notifications/

## 📋 Complete API Endpoints

### Authentication & Profile
```
POST   /api/auth/register/        - Register new user
POST   /api/auth/login/           - Login and get token
POST   /api/auth/logout/          - Logout (invalidate token)
GET    /api/auth/profile/         - Get current user profile
PUT    /api/auth/profile/         - Update profile
```

### Follow System
```
POST   /api/auth/follow/<id>/     - Follow a user
POST   /api/auth/unfollow/<id>/   - Unfollow a user
```

### Posts & Feed
```
GET    /api/posts/                - List all posts
POST   /api/posts/                - Create new post
GET    /api/posts/<id>/           - Get specific post
PUT    /api/posts/<id>/           - Update post (author only)
DELETE /api/posts/<id>/           - Delete post (author only)
GET    /api/feed/                 - Get personalized feed
```

### Likes
```
POST   /api/posts/<id>/like/      - Like a post
POST   /api/posts/<id>/unlike/    - Unlike a post
```

### Comments
```
GET    /api/comments/             - List all comments
POST   /api/comments/             - Create comment
GET    /api/comments/<id>/        - Get specific comment
PUT    /api/comments/<id>/        - Update comment (author only)
DELETE /api/comments/<id>/        - Delete comment (author only)
```

### Notifications
```
GET    /api/notifications/        - Get all notifications
POST   /api/notifications/<id>/read/ - Mark notification as read
```

## 🧪 Testing Workflow

1. **Register Two Users**
   ```bash
   # User 1
   curl -X POST http://localhost:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{"username":"user1","email":"user1@test.com","password":"Pass123","password2":"Pass123"}'
   
   # User 2
   curl -X POST http://localhost:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{"username":"user2","email":"user2@test.com","password":"Pass123","password2":"Pass123"}'
   ```

2. **User 1 Follows User 2**
   ```bash
   curl -X POST http://localhost:8000/api/auth/follow/2/ \
     -H "Authorization: Token USER1_TOKEN"
   ```

3. **User 2 Creates Post**
   ```bash
   curl -X POST http://localhost:8000/api/posts/ \
     -H "Authorization: Token USER2_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title":"Hello","content":"First post!"}'
   ```

4. **User 1 Views Feed** (Should see User 2's post)
   ```bash
   curl -X GET http://localhost:8000/api/feed/ \
     -H "Authorization: Token USER1_TOKEN"
   ```

5. **User 1 Likes Post**
   ```bash
   curl -X POST http://localhost:8000/api/posts/1/like/ \
     -H "Authorization: Token USER1_TOKEN"
   ```

6. **User 2 Checks Notifications** (Should see like notification)
   ```bash
   curl -X GET http://localhost:8000/api/notifications/ \
     -H "Authorization: Token USER2_TOKEN"
   ```

## 📊 Database Models

### User
- Custom user model extending AbstractUser
- Fields: username, email, password, bio, profile_picture, followers

### Post
- Fields: author, title, content, created_at, updated_at
- Relations: Comments, Likes

### Comment
- Fields: post, author, content, created_at, updated_at

### Like
- Fields: user, post, created_at
- Unique: (user, post)

### Notification
- Fields: recipient, actor, verb, target (GenericFK), timestamp, read

## 🔒 Security Features

- Token-based authentication
- Password hashing
- CSRF protection
- Permission-based access control
- Author-only edit/delete permissions
- SQL injection prevention
- XSS protection

## 📦 Dependencies

```
Django==5.2
djangorestframework==3.14.0
django-filter==23.5
Pillow==10.0.0
```

## 🚀 Deployment

See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for:
- Heroku deployment steps
- AWS Elastic Beanstalk setup
- DigitalOcean configuration
- VPS deployment with Nginx/Gunicorn
- SSL certificate setup
- Database migration to PostgreSQL
- Static files configuration
- Monitoring setup

## 📝 Key Implementation Details

### Follow System
- Many-to-many self-referential relationship
- `symmetrical=False` for one-way following
- Automatic notification creation on follow

### Feed Algorithm
- Filters posts by authors in user's following list
- Ordered by creation date (newest first)
- Paginated (10 posts per page)

### Like System
- Unique constraint prevents duplicate likes
- Automatic notification to post author
- No self-notification (user liking own post)

### Notification System
- Uses Django's ContentTypes framework
- GenericForeignKey for flexible target objects
- Supports notifications for any model
- Read/unread tracking

## 🎯 Task Completion Summary

### ✅ Task 2: User Follows and Feed
- [x] User model with followers field
- [x] Follow/unfollow API endpoints
- [x] Feed endpoint with filtering
- [x] Proper permissions
- [x] URL patterns configured
- [x] Documentation complete

### ✅ Task 3: Notifications and Likes
- [x] Like model created
- [x] Notification model with GenericFK
- [x] Like/unlike endpoints
- [x] Notification endpoints
- [x] Automatic notification creation
- [x] Comprehensive testing
- [x] Documentation complete

### ✅ Task 4: Deployment
- [x] Production settings guide
- [x] Multiple hosting options documented
- [x] Security configurations
- [x] Web server setup (Gunicorn/Nginx)
- [x] Static files management
- [x] Database configuration
- [x] Monitoring setup
- [x] Complete deployment guide

## 📖 Additional Resources

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Repository: https://github.com/yourusername/Alx_DjangoLearnLab
- Directory: `social_media_api`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

Part of ALX Django Learning Lab

---

**All three tasks completed successfully!** ✅

For detailed information, see the individual documentation files:
- **FEATURES_DOCUMENTATION.md** - Complete API usage guide
- **DEPLOYMENT_GUIDE.md** - Production deployment steps
- **API_DOCUMENTATION.md** - Original API documentation
