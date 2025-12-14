# Social Media API

A Django REST Framework API for a social media platform with user authentication, posts, comments, following system, likes, and notifications.

## Features

- **User Authentication**: Register, login, JWT token authentication
- **Posts & Comments**: Create, read, update, delete posts and comments
- **User Relationships**: Follow/unfollow other users
- **Personalized Feed**: See posts from users you follow
- **Likes**: Like/unlike posts with notifications
- **Notifications**: Real-time notifications for user interactions
- **Production Ready**: Secure settings, static file handling, deployment configuration

## API Endpoints

### Authentication
- `POST /api/accounts/register/` - Register new user
- `POST /api/accounts/login/` - Login and get token
- `GET /api/accounts/profile/` - Get/update user profile

### Posts & Comments
- `GET /api/posts/` - List all posts (paginated)
- `POST /api/posts/` - Create a new post
- `GET /api/posts/<id>/` - Get specific post
- `PUT/PATCH /api/posts/<id>/` - Update post (author only)
- `DELETE /api/posts/<id>/` - Delete post (author only)
- `POST /api/posts/<id>/like/` - Like a post
- `POST /api/posts/<id>/unlike/` - Unlike a post
- `GET /api/comments/` - List all comments
- `POST /api/comments/` - Create a comment

### User Relationships
- `POST /api/accounts/follow/<user_id>/` - Follow a user
- `POST /api/accounts/unfollow/<user_id>/` - Unfollow a user
- `GET /api/accounts/following/` - List users you follow
- `GET /api/accounts/followers/` - List your followers
- `GET /api/feed/` - Personalized feed of followed users' posts

### Notifications
- `GET /api/notifications/` - Get user notifications
- `GET /api/notifications/unread-count/` - Count unread notifications

## Quick Start

### Prerequisites
- Python 3.11+
- pip package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/social-media-api.git
   cd social-media-api

   