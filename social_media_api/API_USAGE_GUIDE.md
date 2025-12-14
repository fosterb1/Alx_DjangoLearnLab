# Social Media API - Complete Usage Guide

## 🌐 Base URL
```
http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com
```

---

## 📋 Table of Contents
1. [How This API Can Be Used](#how-this-api-can-be-used)
2. [Authentication](#authentication)
3. [Available Endpoints](#available-endpoints)
4. [Usage Examples](#usage-examples)
5. [Integration Examples](#integration-examples)

---

## 🚀 How This API Can Be Used

### **1. Mobile Applications**
Build native iOS/Android apps using:
- **React Native** - Cross-platform mobile development
- **Flutter** - Google's UI toolkit for mobile
- **Swift/Kotlin** - Native iOS/Android development

### **2. Web Applications**
Create responsive web apps with:
- **React.js** - Component-based UI library
- **Vue.js** - Progressive JavaScript framework
- **Angular** - Full-featured framework
- **Next.js** - React framework with SSR

### **3. Desktop Applications**
Build desktop apps using:
- **Electron** - Cross-platform desktop apps
- **Tauri** - Lightweight desktop framework
- **Python (Tkinter/PyQt)** - Native desktop apps

### **4. Third-Party Integrations**
- **Chatbots** - Integrate with Telegram, Discord, Slack
- **IoT Devices** - Connect smart devices
- **Analytics Tools** - Track user behavior
- **Marketing Automation** - Email campaigns, notifications

### **5. Microservices**
- Use as a backend for microservices architecture
- Integrate with other APIs
- Build composite applications

---

## 🔐 Authentication

All authenticated endpoints require a **Token** in the header:

```http
Authorization: Token YOUR_TOKEN_HERE
```

### Get Your Token
**Register or Login** to receive your authentication token.

---

## 📡 Available Endpoints

### **Health Check**
- `GET /` - API health status
- `GET /health/` - Detailed health check

### **Authentication Endpoints**

#### Register New User
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "bio": "Software Developer"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Software Developer"
  },
  "token": "abc123def456ghi789..."
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "token": "abc123def456ghi789...",
  "user_id": 1,
  "username": "johndoe"
}
```

#### Get User Profile
```http
GET /api/auth/profile/
Authorization: Token YOUR_TOKEN
```

#### Logout
```http
POST /api/auth/logout/
Authorization: Token YOUR_TOKEN
```

#### Follow User
```http
POST /api/auth/follow/<user_id>/
Authorization: Token YOUR_TOKEN
```

#### Unfollow User
```http
POST /api/auth/unfollow/<user_id>/
Authorization: Token YOUR_TOKEN
```

---

### **Posts Endpoints**

#### List All Posts
```http
GET /api/posts/
```

**Query Parameters:**
- `?search=keyword` - Search posts
- `?ordering=-created_at` - Sort by date (newest first)
- `?page=2` - Pagination

#### Create Post
```http
POST /api/posts/
Authorization: Token YOUR_TOKEN
Content-Type: application/json

{
  "title": "My First Post",
  "content": "This is my first post on the platform!"
}
```

#### Get Single Post
```http
GET /api/posts/<post_id>/
```

#### Update Post
```http
PUT /api/posts/<post_id>/
Authorization: Token YOUR_TOKEN
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content"
}
```

#### Delete Post
```http
DELETE /api/posts/<post_id>/
Authorization: Token YOUR_TOKEN
```

#### Like Post
```http
POST /api/posts/<post_id>/like/
Authorization: Token YOUR_TOKEN
```

#### Unlike Post
```http
POST /api/posts/<post_id>/unlike/
Authorization: Token YOUR_TOKEN
```

#### Get User Feed
```http
GET /api/feed/
Authorization: Token YOUR_TOKEN
```
*Returns posts from users you follow*

---

### **Comments Endpoints**

#### List Comments
```http
GET /api/comments/
```

**Query Parameters:**
- `?post=<post_id>` - Filter by post

#### Create Comment
```http
POST /api/comments/
Authorization: Token YOUR_TOKEN
Content-Type: application/json

{
  "post": 1,
  "content": "Great post!"
}
```

#### Get Single Comment
```http
GET /api/comments/<comment_id>/
```

#### Update Comment
```http
PUT /api/comments/<comment_id>/
Authorization: Token YOUR_TOKEN
Content-Type: application/json

{
  "content": "Updated comment"
}
```

#### Delete Comment
```http
DELETE /api/comments/<comment_id>/
Authorization: Token YOUR_TOKEN
```

---

### **Notifications Endpoints**

#### Get User Notifications
```http
GET /api/notifications/
Authorization: Token YOUR_TOKEN
```

**Response:**
```json
[
  {
    "id": 1,
    "actor": "johndoe",
    "verb": "liked your post",
    "target": "My First Post",
    "timestamp": "2025-12-14T10:30:00Z",
    "read": false
  }
]
```

---

## 💻 Usage Examples

### **JavaScript/Fetch API**

```javascript
// Register a new user
async function registerUser() {
  const response = await fetch('http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com/api/auth/register/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: 'newuser',
      email: 'newuser@example.com',
      password: 'SecurePass123!',
      password2: 'SecurePass123!',
      bio: 'New to this platform'
    })
  });
  
  const data = await response.json();
  console.log('Token:', data.token);
  localStorage.setItem('token', data.token);
}

// Create a post
async function createPost() {
  const token = localStorage.getItem('token');
  
  const response = await fetch('http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com/api/posts/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${token}`
    },
    body: JSON.stringify({
      title: 'My Post',
      content: 'Post content here'
    })
  });
  
  const post = await response.json();
  console.log('Created post:', post);
}

// Get all posts
async function getPosts() {
  const response = await fetch('http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com/api/posts/');
  const posts = await response.json();
  console.log('Posts:', posts);
}
```

### **Python/Requests**

```python
import requests

BASE_URL = "http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com"

# Register user
def register_user():
    response = requests.post(f"{BASE_URL}/api/auth/register/", json={
        "username": "pythonuser",
        "email": "python@example.com",
        "password": "SecurePass123!",
        "password2": "SecurePass123!",
        "bio": "Python developer"
    })
    data = response.json()
    return data['token']

# Create post
def create_post(token):
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(
        f"{BASE_URL}/api/posts/",
        headers=headers,
        json={
            "title": "Python Post",
            "content": "Created from Python"
        }
    )
    return response.json()

# Get all posts
def get_posts():
    response = requests.get(f"{BASE_URL}/api/posts/")
    return response.json()
```

### **React Example**

```jsx
import React, { useState, useEffect } from 'react';

const BASE_URL = 'http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com';

function PostsList() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${BASE_URL}/api/posts/`)
      .then(res => res.json())
      .then(data => {
        setPosts(data.results || data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error:', error);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Posts</h1>
      {posts.map(post => (
        <div key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
          <small>By: {post.author}</small>
        </div>
      ))}
    </div>
  );
}

export default PostsList;
```

### **React Native Example**

```javascript
import React, { useState } from 'react';
import { View, Text, TextInput, Button, FlatList } from 'react-native';

const BASE_URL = 'http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com';

const SocialMediaApp = () => {
  const [posts, setPosts] = useState([]);
  const [token, setToken] = useState(null);

  const login = async (username, password) => {
    const response = await fetch(`${BASE_URL}/api/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    setToken(data.token);
  };

  const loadPosts = async () => {
    const response = await fetch(`${BASE_URL}/api/posts/`);
    const data = await response.json();
    setPosts(data.results || data);
  };

  return (
    <View>
      <Text>Social Media App</Text>
      <FlatList
        data={posts}
        renderItem={({ item }) => (
          <View>
            <Text>{item.title}</Text>
            <Text>{item.content}</Text>
          </View>
        )}
        keyExtractor={item => item.id.toString()}
      />
    </View>
  );
};

export default SocialMediaApp;
```

### **cURL Examples**

```bash
# Register
curl -X POST http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "curluser",
    "email": "curl@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "bio": "Testing with cURL"
  }'

# Login
curl -X POST http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "curluser",
    "password": "SecurePass123!"
  }'

# Create Post (replace TOKEN)
curl -X POST http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{
    "title": "cURL Post",
    "content": "Posted using cURL"
  }'

# Get Posts
curl http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com/api/posts/
```

---

## 🔗 Integration Examples

### **1. WordPress Plugin**
```php
<?php
function social_media_api_post($title, $content) {
    $token = get_option('social_media_api_token');
    
    $response = wp_remote_post('http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com/api/posts/', array(
        'headers' => array(
            'Authorization' => 'Token ' . $token,
            'Content-Type' => 'application/json'
        ),
        'body' => json_encode(array(
            'title' => $title,
            'content' => $content
        ))
    ));
    
    return wp_remote_retrieve_body($response);
}
?>
```

### **2. Telegram Bot**
```python
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

BASE_URL = "http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com"

def post_command(update: Update, context: CallbackContext):
    user_token = get_user_token(update.effective_user.id)
    text = ' '.join(context.args)
    
    requests.post(
        f"{BASE_URL}/api/posts/",
        headers={'Authorization': f'Token {user_token}'},
        json={'title': 'Telegram Post', 'content': text}
    )
    
    update.message.reply_text('Posted successfully!')
```

### **3. Discord Bot**
```javascript
const Discord = require('discord.js');
const axios = require('axios');

const BASE_URL = 'http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com';

client.on('message', async message => {
  if (message.content.startsWith('!post')) {
    const content = message.content.slice(6);
    
    const response = await axios.post(`${BASE_URL}/api/posts/`, {
      title: 'Discord Post',
      content: content
    }, {
      headers: { 'Authorization': `Token ${userToken}` }
    });
    
    message.reply('Post created!');
  }
});
```

---

## 📊 Response Formats

### Success Response (200/201)
```json
{
  "id": 1,
  "title": "Post Title",
  "content": "Post content",
  "author": "username",
  "created_at": "2025-12-14T10:30:00Z"
}
```

### Error Response (400/401/404)
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

### Paginated Response
```json
{
  "count": 100,
  "next": "http://...?page=2",
  "previous": null,
  "results": [...]
}
```

---

## 🔒 Security Best Practices

1. **Always use HTTPS in production** (when available)
2. **Never expose your token** in client-side code
3. **Store tokens securely** (localStorage, secure storage)
4. **Implement token refresh** for long-lived sessions
5. **Validate all user inputs** before sending to API
6. **Handle errors gracefully** in your application
7. **Use environment variables** for API URLs

---

## 📈 Rate Limiting

Currently, there are no rate limits, but for production use:
- Implement request throttling
- Cache responses when possible
- Use pagination for large datasets
- Batch requests when applicable

---

## 🐛 Troubleshooting

### Common Issues

**1. 401 Unauthorized**
- Check if token is valid
- Ensure Authorization header is properly formatted
- Token may have expired

**2. 404 Not Found**
- Verify the endpoint URL
- Check if resource exists
- Ensure correct HTTP method

**3. 400 Bad Request**
- Validate request body format
- Check required fields
- Ensure correct data types

**4. CORS Errors (Browser)**
- API needs CORS headers configured
- Use proxy in development
- Or configure CORS in Django settings

---

## 📞 Support

- **API URL:** http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com
- **Admin Panel:** http://social-media-api-env.eba-w98jgaun.us-east-1.elasticbeanstalk.com/admin/
- **Database:** PostgreSQL on AWS RDS

---

**Last Updated:** December 14, 2025
