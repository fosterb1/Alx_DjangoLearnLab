# Social Media API - Posts and Comments Documentation

## Overview
This API provides comprehensive functionality for managing posts and comments in a social media platform. Users can create, read, update, and delete posts and comments with proper authentication and authorization.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All write operations (POST, PUT, PATCH, DELETE) require authentication using Token Authentication.

### Authentication Header
```
Authorization: Token <your-token-here>
```

## Pagination
All list endpoints support pagination with the following parameters:
- `page`: Page number (default: 1)
- `page_size`: Number of results per page (default: 10, max: 100)

## Posts Endpoints

### 1. List All Posts
**GET** `/api/posts/`

Retrieve a paginated list of all posts.

**Query Parameters:**
- `page`: Page number
- `page_size`: Results per page
- `search`: Search in title and content
- `author`: Filter by author ID
- `title`: Filter by exact title
- `ordering`: Sort by field (e.g., `-created_at`, `updated_at`)

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/posts/?search=django&page=1&page_size=10"
```

**Example Response:**
```json
{
    "count": 50,
    "next": "http://localhost:8000/api/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": "john_doe",
            "author_id": 1,
            "title": "Getting Started with Django",
            "content": "Django is a powerful web framework...",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "comments": [],
            "comments_count": 0
        }
    ]
}
```

### 2. Create a Post
**POST** `/api/posts/`

Create a new post. Requires authentication.

**Request Body:**
```json
{
    "title": "My New Post",
    "content": "This is the content of my post..."
}
```

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My New Post",
    "content": "This is the content of my post..."
  }'
```

**Example Response:**
```json
{
    "id": 2,
    "author": "john_doe",
    "author_id": 1,
    "title": "My New Post",
    "content": "This is the content of my post...",
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z",
    "comments": [],
    "comments_count": 0
}
```

**Status Codes:**
- `201 Created`: Post created successfully
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Authentication required

### 3. Retrieve a Post
**GET** `/api/posts/{id}/`

Retrieve details of a specific post.

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/posts/1/
```

**Example Response:**
```json
{
    "id": 1,
    "author": "john_doe",
    "author_id": 1,
    "title": "Getting Started with Django",
    "content": "Django is a powerful web framework...",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "comments": [
        {
            "id": 1,
            "post": 1,
            "author": "jane_smith",
            "author_id": 2,
            "content": "Great tutorial!",
            "created_at": "2024-01-15T11:15:00Z",
            "updated_at": "2024-01-15T11:15:00Z"
        }
    ],
    "comments_count": 1
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Post does not exist

### 4. Update a Post
**PUT** `/api/posts/{id}/`

Update an existing post. Only the author can update their post.

**Request Body:**
```json
{
    "title": "Updated Title",
    "content": "Updated content..."
}
```

**Example Request:**
```bash
curl -X PUT http://localhost:8000/api/posts/1/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content..."
  }'
```

**Status Codes:**
- `200 OK`: Post updated successfully
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Not the author
- `404 Not Found`: Post does not exist

### 5. Partial Update a Post
**PATCH** `/api/posts/{id}/`

Partially update a post. Only the author can update their post.

**Request Body:**
```json
{
    "title": "New Title Only"
}
```

**Status Codes:**
- `200 OK`: Post updated successfully
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Not the author
- `404 Not Found`: Post does not exist

### 6. Delete a Post
**DELETE** `/api/posts/{id}/`

Delete a post. Only the author can delete their post.

**Example Request:**
```bash
curl -X DELETE http://localhost:8000/api/posts/1/ \
  -H "Authorization: Token your-token-here"
```

**Status Codes:**
- `204 No Content`: Post deleted successfully
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Not the author
- `404 Not Found`: Post does not exist

## Comments Endpoints

### 1. List All Comments
**GET** `/api/comments/`

Retrieve a paginated list of all comments.

**Query Parameters:**
- `page`: Page number
- `page_size`: Results per page
- `post`: Filter by post ID
- `author`: Filter by author ID
- `ordering`: Sort by field (e.g., `-created_at`, `updated_at`)

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/comments/?post=1&page=1"
```

**Example Response:**
```json
{
    "count": 15,
    "next": "http://localhost:8000/api/comments/?page=2&post=1",
    "previous": null,
    "results": [
        {
            "id": 1,
            "post": 1,
            "author": "jane_smith",
            "author_id": 2,
            "content": "Great post!",
            "created_at": "2024-01-15T11:15:00Z",
            "updated_at": "2024-01-15T11:15:00Z"
        }
    ]
}
```

### 2. Create a Comment
**POST** `/api/comments/`

Create a new comment on a post. Requires authentication.

**Request Body:**
```json
{
    "post": 1,
    "content": "This is my comment on the post"
}
```

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "This is my comment on the post"
  }'
```

**Example Response:**
```json
{
    "id": 2,
    "post": 1,
    "author": "john_doe",
    "author_id": 1,
    "content": "This is my comment on the post",
    "created_at": "2024-01-15T12:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
}
```

**Status Codes:**
- `201 Created`: Comment created successfully
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Authentication required

### 3. Retrieve a Comment
**GET** `/api/comments/{id}/`

Retrieve details of a specific comment.

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/comments/1/
```

**Example Response:**
```json
{
    "id": 1,
    "post": 1,
    "author": "jane_smith",
    "author_id": 2,
    "content": "Great post!",
    "created_at": "2024-01-15T11:15:00Z",
    "updated_at": "2024-01-15T11:15:00Z"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Comment does not exist

### 4. Update a Comment
**PUT** `/api/comments/{id}/`

Update an existing comment. Only the author can update their comment.

**Request Body:**
```json
{
    "post": 1,
    "content": "Updated comment content"
}
```

**Example Request:**
```bash
curl -X PUT http://localhost:8000/api/comments/1/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "Updated comment content"
  }'
```

**Status Codes:**
- `200 OK`: Comment updated successfully
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Not the author
- `404 Not Found`: Comment does not exist

### 5. Partial Update a Comment
**PATCH** `/api/comments/{id}/`

Partially update a comment. Only the author can update their comment.

**Request Body:**
```json
{
    "content": "Updated content only"
}
```

**Status Codes:**
- `200 OK`: Comment updated successfully
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Not the author
- `404 Not Found`: Comment does not exist

### 6. Delete a Comment
**DELETE** `/api/comments/{id}/`

Delete a comment. Only the author can delete their comment.

**Example Request:**
```bash
curl -X DELETE http://localhost:8000/api/comments/1/ \
  -H "Authorization: Token your-token-here"
```

**Status Codes:**
- `204 No Content`: Comment deleted successfully
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Not the author
- `404 Not Found`: Comment does not exist

## Filtering and Search Examples

### Search Posts by Title or Content
```bash
curl -X GET "http://localhost:8000/api/posts/?search=django"
```

### Filter Posts by Author
```bash
curl -X GET "http://localhost:8000/api/posts/?author=1"
```

### Filter Comments by Post
```bash
curl -X GET "http://localhost:8000/api/comments/?post=1"
```

### Sort Posts by Creation Date (Descending)
```bash
curl -X GET "http://localhost:8000/api/posts/?ordering=-created_at"
```

### Sort Posts by Update Date (Ascending)
```bash
curl -X GET "http://localhost:8000/api/posts/?ordering=updated_at"
```

### Combine Multiple Filters
```bash
curl -X GET "http://localhost:8000/api/posts/?search=python&author=1&ordering=-created_at&page_size=20"
```

## Error Responses

### 400 Bad Request
```json
{
    "title": ["This field is required."],
    "content": ["This field is required."]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

## Permissions Summary

| Endpoint | Anonymous | Authenticated | Author Only |
|----------|-----------|---------------|-------------|
| GET /posts/ | ✓ | ✓ | - |
| POST /posts/ | ✗ | ✓ | - |
| GET /posts/{id}/ | ✓ | ✓ | - |
| PUT/PATCH /posts/{id}/ | ✗ | ✗ | ✓ |
| DELETE /posts/{id}/ | ✗ | ✗ | ✓ |
| GET /comments/ | ✓ | ✓ | - |
| POST /comments/ | ✗ | ✓ | - |
| GET /comments/{id}/ | ✓ | ✓ | - |
| PUT/PATCH /comments/{id}/ | ✗ | ✗ | ✓ |
| DELETE /comments/{id}/ | ✗ | ✗ | ✓ |

## Testing with Postman

### Setup
1. Import the API endpoints into Postman
2. Create an environment variable `token` with your authentication token
3. Set the `Authorization` header to `Token {{token}}`

### Test Sequence
1. **Register a user** (if not done already)
2. **Login** to get authentication token
3. **Create a post** using the token
4. **List all posts** to verify creation
5. **Create comments** on the post
6. **Update the post** (as author)
7. **Try to update another user's post** (should fail)
8. **Delete your post**

## Rate Limiting
Currently, no rate limiting is implemented. Consider adding rate limiting for production use.

## CORS
For frontend integration, ensure CORS is properly configured in your Django settings.

## Notes
- All timestamps are in UTC timezone
- Posts and comments are automatically ordered by creation date (newest first)
- Deleting a post will cascade delete all its comments
- The author field is automatically set to the authenticated user
- Search is case-insensitive and searches both title and content fields
