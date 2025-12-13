# Social Media API - Complete Feature Documentation

## Overview
This comprehensive documentation covers all features of the Social Media API including:
- User Authentication and Profile Management
- User Follow/Unfollow System
- Post and Comment Management
- Like/Unlike Functionality
- Notification System
- Personalized Feed

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All authenticated endpoints require Token Authentication.

### Authentication Header
```
Authorization: Token <your-token-here>
```

---

## 1. User Authentication & Profile Management

### Register a New User
**POST** `/api/auth/register/`

**Request Body:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123",
    "password2": "SecurePassword123",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Software developer and tech enthusiast"
}
```

**Response:**
```json
{
    "message": "User registered successfully.",
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "Software developer and tech enthusiast",
        "profile_picture": null,
        "followers": [],
        "followers_count": 0,
        "following_count": 0
    }
}
```

### Login
**POST** `/api/auth/login/`

**Request Body:**
```json
{
    "username": "john_doe",
    "password": "SecurePassword123"
}
```

**Response:**
```json
{
    "message": "User logged in successfully.",
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "bio": "Software developer and tech enthusiast",
        "followers_count": 5,
        "following_count": 10
    }
}
```

### Get User Profile
**GET** `/api/auth/profile/`

Requires authentication. Returns the authenticated user's profile.

**Response:**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Software developer and tech enthusiast",
    "profile_picture": null,
    "followers": [2, 3, 5],
    "followers_count": 3,
    "following_count": 8
}
```

### Update User Profile
**PUT** `/api/auth/profile/`

**Request Body:**
```json
{
    "bio": "Updated bio text",
    "first_name": "John",
    "last_name": "Doe"
}
```

### Logout
**POST** `/api/auth/logout/`

Requires authentication. Deletes the user's authentication token.

---

## 2. Follow/Unfollow System

### Follow a User
**POST** `/api/auth/follow/<user_id>/`

Follow another user by their user ID. Creates a notification for the followed user.

**Example:**
```bash
curl -X POST http://localhost:8000/api/auth/follow/5/ \
  -H "Authorization: Token your-token-here"
```

**Response:**
```json
{
    "message": "You are now following jane_smith."
}
```

**Status Codes:**
- `200 OK`: Successfully followed
- `400 Bad Request`: Already following or trying to follow self
- `401 Unauthorized`: Authentication required
- `404 Not Found`: User does not exist

### Unfollow a User
**POST** `/api/auth/unfollow/<user_id>/`

Unfollow a user you're currently following.

**Example:**
```bash
curl -X POST http://localhost:8000/api/auth/unfollow/5/ \
  -H "Authorization: Token your-token-here"
```

**Response:**
```json
{
    "message": "You have unfollowed jane_smith."
}
```

**Status Codes:**
- `200 OK`: Successfully unfollowed
- `400 Bad Request`: Not following this user or trying to unfollow self
- `401 Unauthorized`: Authentication required
- `404 Not Found`: User does not exist

---

## 3. Posts Management

### List All Posts
**GET** `/api/posts/`

**Query Parameters:**
- `page`: Page number
- `page_size`: Results per page (default: 10, max: 100)
- `search`: Search in title and content
- `author`: Filter by author ID
- `ordering`: Sort by field (e.g., `-created_at`)

**Response:**
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
            "title": "My First Post",
            "content": "This is the content...",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "comments": [],
            "comments_count": 5,
            "likes_count": 12
        }
    ]
}
```

### Create a Post
**POST** `/api/posts/`

Requires authentication.

**Request Body:**
```json
{
    "title": "My New Post",
    "content": "This is the content of my post..."
}
```

### Get Feed (Posts from Followed Users)
**GET** `/api/feed/`

Returns posts from users that the authenticated user follows, ordered by creation date (newest first).

**Example:**
```bash
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Token your-token-here"
```

**Response:**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/feed/?page=2",
    "previous": null,
    "results": [
        {
            "id": 15,
            "author": "jane_smith",
            "author_id": 2,
            "title": "Latest Update",
            "content": "Check out my latest thoughts...",
            "created_at": "2024-01-20T14:30:00Z",
            "updated_at": "2024-01-20T14:30:00Z",
            "comments": [],
            "comments_count": 3,
            "likes_count": 8
        }
    ]
}
```

**Requirements:**
- Must be authenticated
- Returns posts only from users you follow
- Paginated results (10 per page)
- Ordered by creation date (newest first)

### Retrieve/Update/Delete a Post
See API_DOCUMENTATION.md for full CRUD operations on posts.

---

## 4. Comments Management

### Create a Comment
**POST** `/api/comments/`

Creates a comment on a post. Automatically creates a notification for the post author (if different from commenter).

**Request Body:**
```json
{
    "post": 1,
    "content": "Great post! I really enjoyed reading this."
}
```

**Response:**
```json
{
    "id": 5,
    "post": 1,
    "author": "john_doe",
    "author_id": 1,
    "content": "Great post! I really enjoyed reading this.",
    "created_at": "2024-01-15T12:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
}
```

### List/Update/Delete Comments
See API_DOCUMENTATION.md for full CRUD operations on comments.

---

## 5. Likes System

### Like a Post
**POST** `/api/posts/<post_id>/like/`

Like a post. Creates a notification for the post author (if different from the liker).

**Example:**
```bash
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Token your-token-here"
```

**Response:**
```json
{
    "message": "Post liked successfully."
}
```

**Status Codes:**
- `201 Created`: Post liked successfully
- `400 Bad Request`: Already liked this post
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Post does not exist

**Features:**
- Users cannot like the same post twice
- Liking a post creates a notification for the post author
- No notification if user likes their own post

### Unlike a Post
**POST** `/api/posts/<post_id>/unlike/`

Remove your like from a post.

**Example:**
```bash
curl -X POST http://localhost:8000/api/posts/1/unlike/ \
  -H "Authorization: Token your-token-here"
```

**Response:**
```json
{
    "message": "Post unliked successfully."
}
```

**Status Codes:**
- `200 OK`: Post unliked successfully
- `400 Bad Request`: You have not liked this post
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Post does not exist

---

## 6. Notifications System

### Get All Notifications
**GET** `/api/notifications/`

Retrieve all notifications for the authenticated user, ordered by timestamp (newest first).

**Example:**
```bash
curl -X GET http://localhost:8000/api/notifications/ \
  -H "Authorization: Token your-token-here"
```

**Response:**
```json
{
    "count": 15,
    "next": "http://localhost:8000/api/notifications/?page=2",
    "previous": null,
    "results": [
        {
            "id": 10,
            "recipient": 1,
            "actor": "jane_smith",
            "actor_id": 2,
            "verb": "liked your post",
            "target_content_type": 8,
            "target_object_id": 5,
            "timestamp": "2024-01-20T15:30:00Z",
            "read": false
        },
        {
            "id": 9,
            "recipient": 1,
            "actor": "bob_wilson",
            "actor_id": 3,
            "verb": "started following you",
            "target_content_type": 4,
            "target_object_id": 3,
            "timestamp": "2024-01-20T14:20:00Z",
            "read": false
        },
        {
            "id": 8,
            "recipient": 1,
            "actor": "alice_jones",
            "actor_id": 4,
            "verb": "commented on your post",
            "target_content_type": 9,
            "target_object_id": 12,
            "timestamp": "2024-01-20T13:10:00Z",
            "read": true
        }
    ]
}
```

### Mark Notification as Read
**POST** `/api/notifications/<notification_id>/read/`

Mark a specific notification as read.

**Example:**
```bash
curl -X POST http://localhost:8000/api/notifications/10/read/ \
  -H "Authorization: Token your-token-here"
```

**Response:**
```json
{
    "message": "Notification marked as read."
}
```

**Status Codes:**
- `200 OK`: Notification marked as read
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Notification not found or doesn't belong to user

### Notification Types

Notifications are automatically created for the following events:

1. **New Follower**
   - Verb: "started following you"
   - Created when someone follows you
   
2. **Post Liked**
   - Verb: "liked your post"
   - Created when someone likes your post
   
3. **Post Commented**
   - Verb: "commented on your post"
   - Created when someone comments on your post

**Note:** Notifications are NOT created when:
- You like your own post
- You comment on your own post
- You follow yourself (this action is prevented)

---

## Complete API Endpoints Summary

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login user | No |
| POST | `/api/auth/logout/` | Logout user | Yes |
| GET | `/api/auth/profile/` | Get user profile | Yes |
| PUT | `/api/auth/profile/` | Update profile | Yes |

### Follow System
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/follow/<user_id>/` | Follow a user | Yes |
| POST | `/api/auth/unfollow/<user_id>/` | Unfollow a user | Yes |

### Posts
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/posts/` | List all posts | No |
| POST | `/api/posts/` | Create a post | Yes |
| GET | `/api/posts/<id>/` | Get a post | No |
| PUT/PATCH | `/api/posts/<id>/` | Update a post | Yes (Author) |
| DELETE | `/api/posts/<id>/` | Delete a post | Yes (Author) |
| GET | `/api/feed/` | Get posts from followed users | Yes |

### Comments
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/comments/` | List all comments | No |
| POST | `/api/comments/` | Create a comment | Yes |
| GET | `/api/comments/<id>/` | Get a comment | No |
| PUT/PATCH | `/api/comments/<id>/` | Update a comment | Yes (Author) |
| DELETE | `/api/comments/<id>/` | Delete a comment | Yes (Author) |

### Likes
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/posts/<id>/like/` | Like a post | Yes |
| POST | `/api/posts/<id>/unlike/` | Unlike a post | Yes |

### Notifications
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/notifications/` | Get all notifications | Yes |
| POST | `/api/notifications/<id>/read/` | Mark as read | Yes |

---

## Testing Guide

### 1. Test User Registration and Authentication
```bash
# Register User 1
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "email": "user1@example.com",
    "password": "Password123",
    "password2": "Password123",
    "bio": "I am user 1"
  }'

# Register User 2
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user2",
    "email": "user2@example.com",
    "password": "Password123",
    "password2": "Password123",
    "bio": "I am user 2"
  }'
```

### 2. Test Follow System
```bash
# User 1 follows User 2 (use User 1's token)
curl -X POST http://localhost:8000/api/auth/follow/2/ \
  -H "Authorization: Token <user1-token>"

# Check User 2's notifications (should see "started following you")
curl -X GET http://localhost:8000/api/notifications/ \
  -H "Authorization: Token <user2-token>"
```

### 3. Test Post Creation and Feed
```bash
# User 2 creates a post
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token <user2-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Hello World",
    "content": "This is my first post!"
  }'

# User 1 views feed (should see User 2's post)
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Token <user1-token>"
```

### 4. Test Likes and Notifications
```bash
# User 1 likes User 2's post
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Token <user1-token>"

# Check User 2's notifications (should see "liked your post")
curl -X GET http://localhost:8000/api/notifications/ \
  -H "Authorization: Token <user2-token>"
```

### 5. Test Comments and Notifications
```bash
# User 1 comments on User 2's post
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Token <user1-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "Great post!"
  }'

# Check User 2's notifications (should see "commented on your post")
curl -X GET http://localhost:8000/api/notifications/ \
  -H "Authorization: Token <user2-token>"
```

---

## Database Models

### User Model
- Extends Django's AbstractUser
- Additional fields: `bio`, `profile_picture`, `followers` (ManyToMany self-referential)

### Post Model
- Fields: `author`, `title`, `content`, `created_at`, `updated_at`
- Related: Comments, Likes

### Comment Model
- Fields: `post`, `author`, `content`, `created_at`, `updated_at`

### Like Model
- Fields: `user`, `post`, `created_at`
- Unique constraint: (user, post)

### Notification Model
- Fields: `recipient`, `actor`, `verb`, `target` (GenericForeignKey), `timestamp`, `read`
- Supports notifications for any model via ContentTypes

---

## Permissions Summary

| Feature | Anonymous | Authenticated | Author/Owner Only |
|---------|-----------|---------------|-------------------|
| View Posts/Comments | ✓ | ✓ | - |
| Create Post/Comment | ✗ | ✓ | - |
| Edit Post/Comment | ✗ | ✗ | ✓ |
| Delete Post/Comment | ✗ | ✗ | ✓ |
| Like/Unlike Post | ✗ | ✓ | - |
| Follow/Unfollow | ✗ | ✓ | - |
| View Feed | ✗ | ✓ | - |
| View Notifications | ✗ | ✓ (own only) | - |

---

## Best Practices

1. **Always use HTTPS** in production
2. **Rate limiting** should be implemented for production
3. **Input validation** is handled by Django REST Framework serializers
4. **Pagination** is enabled by default (10 items per page)
5. **Timestamps** are in UTC timezone
6. **Cascade deletes**: Deleting a post deletes all associated comments, likes, and notifications

---

## Error Handling

All endpoints return appropriate HTTP status codes and error messages:

- `200 OK`: Success
- `201 Created`: Resource created
- `204 No Content`: Resource deleted
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Example error response:
```json
{
    "error": "You cannot follow yourself.",
    "detail": "Invalid operation"
}
```
