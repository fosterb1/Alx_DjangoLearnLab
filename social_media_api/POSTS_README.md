# Posts and Comments Functionality

## Overview
This module implements comprehensive posts and comments functionality for the Social Media API, allowing users to create, read, update, and delete posts and engage with them through comments.

## Features Implemented

### Posts
- ✅ Create posts with title and content
- ✅ List all posts with pagination
- ✅ Retrieve individual post details
- ✅ Update posts (only by author)
- ✅ Delete posts (only by author)
- ✅ Search posts by title or content
- ✅ Filter posts by author
- ✅ Automatic timestamp tracking (created_at, updated_at)
- ✅ Author relationship with User model

### Comments
- ✅ Create comments on posts
- ✅ List all comments with pagination
- ✅ Retrieve individual comment details
- ✅ Update comments (only by author)
- ✅ Delete comments (only by author)
- ✅ Filter comments by post or author
- ✅ Automatic timestamp tracking
- ✅ Cascade deletion when post is deleted

### Security & Permissions
- ✅ Token-based authentication
- ✅ Custom permission class (IsAuthorOrReadOnly)
- ✅ Read-only access for unauthenticated users
- ✅ Write operations require authentication
- ✅ Update/delete restricted to content authors

### Advanced Features
- ✅ Pagination with customizable page size
- ✅ Full-text search on posts
- ✅ Filtering by multiple fields
- ✅ Ordering/sorting capabilities
- ✅ Comments count on posts
- ✅ Nested comments in post detail view

## Project Structure

```
posts/
├── __init__.py
├── admin.py              # Admin interface configuration
├── apps.py               # App configuration
├── models.py             # Post and Comment models
├── serializers.py        # DRF serializers
├── views.py              # ViewSets for API endpoints
├── urls.py               # URL routing
├── tests.py              # Comprehensive test suite
└── migrations/
    └── 0001_initial.py   # Database migrations
```

## Models

### Post Model
```python
class Post(models.Model):
    author = ForeignKey(User)      # Post creator
    title = CharField(max_length=200)
    content = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

### Comment Model
```python
class Comment(models.Model):
    post = ForeignKey(Post)        # Associated post
    author = ForeignKey(User)      # Comment creator
    content = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

## API Endpoints

### Posts
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create a new post (authenticated)
- `GET /api/posts/{id}/` - Get post detail
- `PUT /api/posts/{id}/` - Update post (author only)
- `PATCH /api/posts/{id}/` - Partial update (author only)
- `DELETE /api/posts/{id}/` - Delete post (author only)

### Comments
- `GET /api/comments/` - List all comments
- `POST /api/comments/` - Create a new comment (authenticated)
- `GET /api/comments/{id}/` - Get comment detail
- `PUT /api/comments/{id}/` - Update comment (author only)
- `PATCH /api/comments/{id}/` - Partial update (author only)
- `DELETE /api/comments/{id}/` - Delete comment (author only)

## Installation & Setup

### 1. Install Dependencies
```bash
pip install djangorestframework django-filter
```

### 2. Add to INSTALLED_APPS
Already configured in `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'django_filters',
    'posts',
]
```

### 3. Run Migrations
```bash
python manage.py makemigrations posts
python manage.py migrate
```

### 4. Start Development Server
```bash
python manage.py runserver
```

## Usage Examples

### Create a Post
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "Hello, World!"
  }'
```

### List Posts with Search
```bash
curl "http://localhost:8000/api/posts/?search=django&page=1"
```

### Create a Comment
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "Great post!"
  }'
```

### Filter Comments by Post
```bash
curl "http://localhost:8000/api/comments/?post=1"
```

## Testing

### Run All Tests
```bash
python manage.py test posts
```

### Test Coverage
The test suite includes:
- ✅ Model creation and validation
- ✅ API endpoint functionality
- ✅ Authentication requirements
- ✅ Permission enforcement
- ✅ Filtering and search
- ✅ Pagination
- ✅ CRUD operations for both posts and comments

### Sample Test Results
```
Found 17 test(s).
...............
----------------------------------------------------------------------
Ran 17 tests in 17.335s

OK
```

## Configuration

### REST Framework Settings
Located in `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### Pagination Settings
- Default page size: 10 items
- Max page size: 100 items
- Customizable via `page_size` query parameter

## Query Parameters

### Posts Endpoints
| Parameter | Type | Description |
|-----------|------|-------------|
| page | integer | Page number |
| page_size | integer | Items per page (max 100) |
| search | string | Search in title and content |
| author | integer | Filter by author ID |
| title | string | Filter by exact title |
| ordering | string | Sort field (e.g., -created_at) |

### Comments Endpoints
| Parameter | Type | Description |
|-----------|------|-------------|
| page | integer | Page number |
| page_size | integer | Items per page (max 100) |
| post | integer | Filter by post ID |
| author | integer | Filter by author ID |
| ordering | string | Sort field (e.g., -created_at) |

## Admin Interface

The admin interface is configured with:
- List displays with key fields
- Search functionality
- Filters by date and author
- Read-only timestamp fields

Access at: `http://localhost:8000/admin/posts/`

## Permissions Matrix

| Action | Unauthenticated | Authenticated | Author |
|--------|----------------|---------------|--------|
| List | ✓ | ✓ | ✓ |
| Create | ✗ | ✓ | ✓ |
| Read | ✓ | ✓ | ✓ |
| Update | ✗ | ✗ | ✓ |
| Delete | ✗ | ✗ | ✓ |

## Error Handling

The API returns appropriate HTTP status codes:
- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation errors
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found

## Best Practices

1. **Always authenticate** for write operations
2. **Use pagination** for list endpoints
3. **Validate input** before submission
4. **Handle errors** gracefully in client code
5. **Use search and filters** to reduce response size
6. **Check permissions** before attempting updates/deletes

## Future Enhancements

Potential improvements:
- [ ] Add post categories/tags
- [ ] Implement nested comments (replies)
- [ ] Add like/reaction system
- [ ] Implement content moderation
- [ ] Add image uploads for posts
- [ ] Implement draft posts
- [ ] Add rich text editor support
- [ ] Implement post sharing
- [ ] Add mention/tagging users
- [ ] Rate limiting for API endpoints

## Troubleshooting

### Common Issues

**Issue: 401 Unauthorized**
- Ensure you're including the authentication token
- Format: `Authorization: Token YOUR_TOKEN`

**Issue: 403 Forbidden**
- Verify you're the author of the content
- Check user permissions

**Issue: 404 Not Found**
- Verify the resource ID exists
- Check URL formatting

**Issue: Pagination not working**
- Ensure `page` parameter is positive integer
- Check `page_size` is within limits (1-100)

## Contributing

When contributing to this module:
1. Write tests for new features
2. Follow Django/DRF best practices
3. Update documentation
4. Ensure all tests pass
5. Use proper commit messages

## License

This project is part of the Alx_DjangoLearnLab repository.

## Support

For issues or questions:
- Check the API documentation
- Review test cases for examples
- Consult Django REST Framework documentation
