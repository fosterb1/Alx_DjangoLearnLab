# Social Media API - Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Applications                      │
│              (Web, Mobile, Postman, cURL)                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP/HTTPS
                     │ Token: <auth-token>
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Django REST Framework                     │
│                  (Authentication Layer)                      │
│              Token Authentication Middleware                 │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌────────────────┐      ┌────────────────┐
│   Accounts     │      │     Posts      │
│     App        │      │      App       │
│                │      │                │
│ - User Auth    │      │ - Posts CRUD   │
│ - Profile      │      │ - Comments     │
│ - Follow       │      │ - Likes        │
│                │      │ - Feed         │
└────────┬───────┘      └────────┬───────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌────────────────────┐
         │   Notifications    │
         │       App          │
         │                    │
         │ - Create           │
         │ - List             │
         │ - Mark Read        │
         └──────────┬─────────┘
                    │
                    ▼
         ┌────────────────────┐
         │     Database       │
         │  (SQLite/PostgreSQL)│
         │                    │
         │ - Users            │
         │ - Posts            │
         │ - Comments         │
         │ - Likes            │
         │ - Notifications    │
         └────────────────────┘
```

## User Authentication Flow

```
┌──────┐                           ┌──────────┐
│Client│                           │  Server  │
└──┬───┘                           └────┬─────┘
   │                                    │
   │ POST /api/auth/register/          │
   │ {username, email, password}       │
   ├──────────────────────────────────►│
   │                                    │
   │                           ┌────────▼────────┐
   │                           │ Create User     │
   │                           │ Hash Password   │
   │                           │ Generate Token  │
   │                           └────────┬────────┘
   │                                    │
   │ 201 Created                       │
   │ {token, user_data}                │
   │◄──────────────────────────────────┤
   │                                    │
   │ POST /api/auth/login/             │
   │ {username, password}              │
   ├──────────────────────────────────►│
   │                                    │
   │                           ┌────────▼────────┐
   │                           │ Authenticate    │
   │                           │ Return Token    │
   │                           └────────┬────────┘
   │                                    │
   │ 200 OK                            │
   │ {token, user_data}                │
   │◄──────────────────────────────────┤
   │                                    │
   │ All subsequent requests:           │
   │ Authorization: Token <token>      │
   ├──────────────────────────────────►│
   │                                    │
```

## Follow System Flow

```
User A                  Server                    User B
  │                       │                         │
  │ POST /follow/<B_id>/  │                         │
  ├──────────────────────►│                         │
  │                       │                         │
  │              ┌────────▼────────┐               │
  │              │ Check if A==B   │               │
  │              │ (prevent self)  │               │
  │              └────────┬────────┘               │
  │                       │                         │
  │              ┌────────▼────────┐               │
  │              │ Check duplicate │               │
  │              │ follow          │               │
  │              └────────┬────────┘               │
  │                       │                         │
  │              ┌────────▼────────┐               │
  │              │ Add to          │               │
  │              │ A.following     │               │
  │              └────────┬────────┘               │
  │                       │                         │
  │              ┌────────▼────────┐               │
  │              │ Create          │               │
  │              │ Notification    │               │
  │              └────────┬────────┘               │
  │                       │                         │
  │ 200 OK                │   Notification Created  │
  │ "Now following B"     │                         │
  │◄──────────────────────┤────────────────────────►│
  │                       │                         │
```

## Feed Generation Flow

```
User               Server                    Database
  │                  │                           │
  │ GET /api/feed/   │                           │
  ├─────────────────►│                           │
  │                  │                           │
  │         ┌────────▼────────┐                 │
  │         │ Get current     │                 │
  │         │ user            │                 │
  │         └────────┬────────┘                 │
  │                  │                           │
  │                  │ Query: user.following    │
  │                  ├──────────────────────────►│
  │                  │                           │
  │                  │ [user2, user5, user8]    │
  │                  │◄──────────────────────────┤
  │                  │                           │
  │         ┌────────▼────────┐                 │
  │         │ Filter posts    │                 │
  │         │ by authors in   │                 │
  │         │ following list  │                 │
  │         └────────┬────────┘                 │
  │                  │                           │
  │                  │ Query: Posts where        │
  │                  │ author IN [2,5,8]        │
  │                  ├──────────────────────────►│
  │                  │                           │
  │                  │ [post15, post12, post9]  │
  │                  │◄──────────────────────────┤
  │                  │                           │
  │         ┌────────▼────────┐                 │
  │         │ Order by        │                 │
  │         │ created_at DESC │                 │
  │         │ Paginate        │                 │
  │         └────────┬────────┘                 │
  │                  │                           │
  │ 200 OK           │                           │
  │ {results: [...]} │                           │
  │◄─────────────────┤                           │
  │                  │                           │
```

## Like & Notification Flow

```
User A            Server              User B (Post Author)
  │                 │                         │
  │ POST /posts/1/  │                         │
  │ like/           │                         │
  ├────────────────►│                         │
  │                 │                         │
  │        ┌────────▼────────┐               │
  │        │ Check if A==B   │               │
  │        │ (post author)   │               │
  │        └────────┬────────┘               │
  │                 │                         │
  │        ┌────────▼────────┐               │
  │        │ Create Like     │               │
  │        │ (user=A,post=1) │               │
  │        │ unique check    │               │
  │        └────────┬────────┘               │
  │                 │                         │
  │                 │ IF A != B:              │
  │        ┌────────▼────────┐               │
  │        │ Create          │               │
  │        │ Notification    │               │
  │        │ recipient=B     │               │
  │        │ actor=A         │               │
  │        │ verb="liked"    │               │
  │        └────────┬────────┘               │
  │                 │                         │
  │ 201 Created     │   Notification added    │
  │ "Post liked"    │   to B's notifications  │
  │◄────────────────┤────────────────────────►│
  │                 │                         │
  │                 │ B: GET /notifications/  │
  │                 │◄────────────────────────┤
  │                 │                         │
  │                 │ {actor: "A",            │
  │                 │  verb: "liked",         │
  │                 │  read: false}           │
  │                 ├────────────────────────►│
  │                 │                         │
```

## Comment & Notification Flow

```
User A            Server              User B (Post Author)
  │                 │                         │
  │ POST /comments/ │                         │
  │ {post:1,        │                         │
  │  content:"..."}│                         │
  ├────────────────►│                         │
  │                 │                         │
  │        ┌────────▼────────┐               │
  │        │ Create Comment  │               │
  │        │ author=A        │               │
  │        │ post=1          │               │
  │        └────────┬────────┘               │
  │                 │                         │
  │        ┌────────▼────────┐               │
  │        │ Get post.author │               │
  │        │ (User B)        │               │
  │        └────────┬────────┘               │
  │                 │                         │
  │                 │ IF A != B:              │
  │        ┌────────▼────────┐               │
  │        │ Create          │               │
  │        │ Notification    │               │
  │        │ recipient=B     │               │
  │        │ actor=A         │               │
  │        │ verb="commented"│               │
  │        └────────┬────────┘               │
  │                 │                         │
  │ 201 Created     │   Notification created  │
  │ {comment_data}  │                         │
  │◄────────────────┤────────────────────────►│
  │                 │                         │
```

## Complete User Journey

```
1. REGISTRATION
   Client → POST /api/auth/register/
        → Server creates user + token
        → Response: {token, user_data}

2. LOGIN
   Client → POST /api/auth/login/
        → Server validates credentials
        → Response: {token, user_data}

3. CREATE POST
   Client → POST /api/posts/
        → Headers: Authorization: Token <token>
        → Body: {title, content}
        → Server creates post with author=current_user
        → Response: {post_data}

4. FOLLOW ANOTHER USER
   Client → POST /api/auth/follow/<user_id>/
        → Server adds to following list
        → Server creates notification for followed user
        → Response: "Now following {username}"

5. VIEW FEED
   Client → GET /api/feed/
        → Server filters posts by followed users
        → Response: {results: [posts...]}

6. LIKE A POST
   Client → POST /api/posts/<id>/like/
        → Server creates Like record
        → Server creates notification for post author
        → Response: "Post liked"

7. COMMENT ON POST
   Client → POST /api/comments/
        → Body: {post: id, content: "..."}
        → Server creates comment
        → Server creates notification for post author
        → Response: {comment_data}

8. CHECK NOTIFICATIONS
   Client → GET /api/notifications/
        → Server returns user's notifications
        → Response: {results: [notifications...]}

9. MARK NOTIFICATION READ
   Client → POST /api/notifications/<id>/read/
        → Server updates notification.read = True
        → Response: "Marked as read"
```

## Database Relationships

```
┌──────────────┐
│     User     │
│──────────────│
│ id (PK)      │
│ username     │
│ email        │
│ bio          │
└──────┬───────┘
       │
       │ followers (M2M self)
       │
       ├────────────────────┐
       │                    │
       ▼                    ▼
┌──────────────┐    ┌──────────────┐
│     Post     │    │   Comment    │
│──────────────│    │──────────────│
│ id (PK)      │◄───┤ id (PK)      │
│ author (FK)  │    │ post (FK)    │
│ title        │    │ author (FK)  │
│ content      │    │ content      │
└──────┬───────┘    └──────────────┘
       │
       ▼
┌──────────────┐
│     Like     │
│──────────────│
│ id (PK)      │
│ user (FK)    │
│ post (FK)    │
│ UNIQUE(user, │
│        post) │
└──────────────┘

┌─────────────────┐
│  Notification   │
│─────────────────│
│ id (PK)         │
│ recipient (FK)  │───► User
│ actor (FK)      │───► User
│ verb            │
│ target (GenericFK) ──► Post/Comment/User
│ timestamp       │
│ read            │
└─────────────────┘
```

## Notification Types Matrix

```
Event           Actor    Recipient    Verb                 Target
─────────────────────────────────────────────────────────────────
Follow          User A   User B       "started following"  User B
Like Post       User A   Post Author  "liked your post"    Post
Comment Post    User A   Post Author  "commented on post"  Comment

Self-actions DO NOT create notifications:
- User liking own post
- User commenting on own post
```

## Permission Flow

```
Request → Authentication Check
              │
              ├─ Authenticated? ──No──► 401 Unauthorized
              │
              Yes
              │
              ▼
         Permission Check
              │
              ├─ Has Permission? ──No──► 403 Forbidden
              │
              Yes
              │
              ▼
         Execute View
              │
              ▼
         Return Response
```

## Pagination Flow

```
Client Request: GET /api/posts/?page=2&page_size=10

Server Process:
1. Get all posts matching criteria
2. Order by -created_at
3. Count total results
4. Calculate page range (11-20)
5. Slice queryset [10:20]
6. Serialize results

Response:
{
  "count": 50,
  "next": "http://.../?page=3",
  "previous": "http://.../?page=1",
  "results": [10 posts...]
}
```

## Error Handling Flow

```
Request
  │
  ▼
Try: Execute View
  │
  ├─ Success ──────► 200/201 Response
  │
  ├─ ValidationError ──► 400 Bad Request
  │                     {errors: [...]}
  │
  ├─ AuthenticationError ──► 401 Unauthorized
  │                          {detail: "..."}
  │
  ├─ PermissionError ──► 403 Forbidden
  │                      {detail: "..."}
  │
  ├─ NotFound ──────► 404 Not Found
  │                   {detail: "Not found"}
  │
  └─ ServerError ───► 500 Internal Error
                       {detail: "..."}
```

---

## Quick Reference

### Status Codes
- 200 OK - Success
- 201 Created - Resource created
- 204 No Content - Deleted
- 400 Bad Request - Invalid data
- 401 Unauthorized - Auth required
- 403 Forbidden - No permission
- 404 Not Found - Resource missing
- 500 Server Error - Internal error

### Authentication
- Header: `Authorization: Token <token>`
- Required for: POST, PUT, PATCH, DELETE
- Optional for: GET (some endpoints)

### Common Patterns
- List: GET /resource/
- Create: POST /resource/
- Detail: GET /resource/<id>/
- Update: PUT/PATCH /resource/<id>/
- Delete: DELETE /resource/<id>/
- Action: POST /resource/<id>/action/
