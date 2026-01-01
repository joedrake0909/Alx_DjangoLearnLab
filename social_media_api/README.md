# Social Media API

A Django REST Framework-based Social Media API with user authentication, token-based authorization, and user profile management.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [User Model](#user-model)
- [Testing the API](#testing-the-api)
- [Authentication](#authentication)

## Features

- **Custom User Model**: Extended Django's AbstractUser with additional fields
- **Token Authentication**: Secure token-based authentication using Django REST Framework
- **User Registration**: New users can register with username, email, and password
- **User Login**: Existing users can log in and receive an authentication token
- **Profile Management**: Authenticated users can view and update their profile
- **Posts & Comments**: Create, list, update, and delete posts and comments with ownership checks
- **Search & Pagination**: Search posts by title/content and paginate post/comment lists

## Technologies Used

- **Django 5.2.8**: High-level Python web framework
- **Django REST Framework 3.16.1**: Powerful toolkit for building Web APIs
- **SQLite**: Default database for development
- **Pillow 12.0.0**: Python Imaging Library for image field support

## Project Structure

```
social_media_api/
├── manage.py
├── db.sqlite3
├── accounts/
│   ├── __init__.py
│   ├── admin.py          # Admin configuration for CustomUser
│   ├── apps.py
│   ├── models.py         # CustomUser model definition
│   ├── serializers.py    # DRF serializers for authentication
│   ├── views.py          # API views for registration, login, profile
│   ├── urls.py           # URL routing for accounts app
│   ├── tests.py
│   └── migrations/
│       └── 0001_initial.py
├── posts/
│   ├── __init__.py
│   ├── admin.py          # Admin configuration for Post/Comment
│   ├── apps.py
│   ├── models.py         # Post and Comment models
│   ├── serializers.py    # DRF serializers for posts/comments
│   ├── views.py          # ViewSets for posts/comments with permissions
│   ├── urls.py           # Router registrations
│   └── migrations/
│       └── 0001_initial.py
└── social_media_api/
    ├── __init__.py
    ├── settings.py       # Project settings
    ├── urls.py           # Main URL configuration
    ├── asgi.py
    └── wsgi.py
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### 2. Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd social_media_api
   ```

2. **Install required packages:**
   ```bash
   pip install django djangorestframework Pillow
   ```

3. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Base URL: `http://127.0.0.1:8000/api/`

**Accounts**

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/accounts/register/` | POST | Register a new user | No |
| `/api/accounts/login/` | POST | Login and receive token | No |
| `/api/accounts/profile/` | GET | Retrieve user profile | Yes |
| `/api/accounts/profile/` | PUT/PATCH | Update user profile | Yes |

**Posts**

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/posts/` | GET | List posts (paginated, searchable by `search` query) | Yes |
| `/api/posts/` | POST | Create a post (title, content) | Yes |
| `/api/posts/{id}/` | GET | Retrieve a single post | Yes |
| `/api/posts/{id}/` | PUT/PATCH | Update your own post | Yes |
| `/api/posts/{id}/` | DELETE | Delete your own post | Yes |

**Comments**

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/comments/` | GET | List comments (filter by `?post=<post_id>`) | Yes |
| `/api/comments/` | POST | Create a comment on a post | Yes |
| `/api/comments/{id}/` | GET | Retrieve a single comment | Yes |
| `/api/comments/{id}/` | PUT/PATCH | Update your own comment | Yes |
| `/api/comments/{id}/` | DELETE | Delete your own comment | Yes |

### Endpoint Details

#### 1. User Registration
**POST** `/api/accounts/register/`

**Request Body:**
```json
{
    "username": "johndoe",
    "email": "johndoe@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "bio": "Hello, I'm John!"
}
```

**Response (201 Created):**
```json
{
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@example.com"
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "message": "User registered successfully"
}
```

#### 2. User Login
**POST** `/api/accounts/login/`

**Request Body:**
```json
{
    "username": "johndoe",
    "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@example.com"
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "message": "Login successful"
}
```

#### 3. Get User Profile
**GET** `/api/accounts/profile/`

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "johndoe@example.com",
    "bio": "Hello, I'm John!",
    "profile_picture": null,
    "followers_count": 0,
    "following_count": 0,
    "date_joined": "2026-01-01T10:30:00Z"
}
```

#### 4. Update User Profile
**PUT/PATCH** `/api/accounts/profile/`

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Request Body (PATCH):**
```json
{
    "bio": "Updated bio text",
    "email": "newemail@example.com"
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "newemail@example.com",
    "bio": "Updated bio text",
    "profile_picture": null,
    "followers_count": 0,
    "following_count": 0,
    "date_joined": "2026-01-01T10:30:00Z"
}
```

#### 5. Create a Post
**POST** `/api/posts/`

**Request Body:**
```json
{
    "title": "My first post",
    "content": "This is the body of the post"
}
```

**Response (201 Created):**
```json
{
    "id": 10,
    "author": 1,
    "author_username": "johndoe",
    "title": "My first post",
    "content": "This is the body of the post",
    "created_at": "2026-01-01T12:00:00Z",
    "updated_at": "2026-01-01T12:00:00Z"
}
```

#### 6. List Posts (paginated + search)
**GET** `/api/posts/?search=first`

**Response (200 OK):**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 10,
            "author": 1,
            "author_username": "johndoe",
            "title": "My first post",
            "content": "This is the body of the post",
            "created_at": "2026-01-01T12:00:00Z",
            "updated_at": "2026-01-01T12:00:00Z"
        }
    ]
}
```

#### 7. Comment on a Post
**POST** `/api/comments/`

**Request Body:**
```json
{
    "post": 10,
    "content": "Nice post!"
}
```

**Response (201 Created):**
```json
{
    "id": 5,
    "post": 10,
    "author": 1,
    "author_username": "johndoe",
    "content": "Nice post!",
    "created_at": "2026-01-01T12:05:00Z",
    "updated_at": "2026-01-01T12:05:00Z"
}
```

## User Model

The `CustomUser` model extends Django's `AbstractUser` with the following additional fields:

### Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `username` | CharField | Unique username (inherited) | Yes |
| `email` | EmailField | User's email address (inherited) | Yes |
| `password` | CharField | Hashed password (inherited) | Yes |
| `first_name` | CharField | User's first name (inherited) | No |
| `last_name` | CharField | User's last name (inherited) | No |
| `bio` | TextField | User biography (max 500 chars) | No |
| `profile_picture` | ImageField | Profile picture image | No |
| `followers` | ManyToManyField | Users following this user | No |
| `date_joined` | DateTimeField | Account creation date (inherited) | Auto |

### Relationships

- **followers**: A Many-to-Many relationship with itself (symmetrical=False)
  - `user.followers.all()` - Get all followers of a user
  - `user.following.all()` - Get all users that this user follows

## Testing the API

### Using cURL

**Register a new user:**
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"testpass123\",\"password_confirm\":\"testpass123\"}"
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"password\":\"testpass123\"}"
```

**Get profile (replace TOKEN with your actual token):**
```bash
curl -X GET http://127.0.0.1:8000/api/accounts/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Using Postman

1. **Register:**
   - Method: POST
   - URL: `http://127.0.0.1:8000/api/accounts/register/`
   - Body (JSON):
     ```json
     {
         "username": "testuser",
         "email": "test@example.com",
         "password": "testpass123",
         "password_confirm": "testpass123"
     }
     ```

2. **Login:**
   - Method: POST
   - URL: `http://127.0.0.1:8000/api/accounts/login/`
   - Body (JSON):
     ```json
     {
         "username": "testuser",
         "password": "testpass123"
     }
     ```
   - Copy the token from the response

3. **Get Profile:**
   - Method: GET
   - URL: `http://127.0.0.1:8000/api/accounts/profile/`
   - Headers: 
     - Key: `Authorization`
     - Value: `Token YOUR_TOKEN_HERE`

4. **Update Profile:**
   - Method: PATCH
   - URL: `http://127.0.0.1:8000/api/accounts/profile/`
   - Headers: 
     - Key: `Authorization`
     - Value: `Token YOUR_TOKEN_HERE`
   - Body (JSON):
     ```json
     {
         "bio": "My updated bio"
     }
     ```

## Authentication

This API uses **Token Authentication** provided by Django REST Framework.

### How it works:

1. **Registration/Login**: When a user registers or logs in, they receive a unique authentication token
2. **Authenticated Requests**: Include the token in the `Authorization` header for protected endpoints
3. **Header Format**: `Authorization: Token <your-token-here>`

### Token Management:

- Tokens are automatically created upon user registration
- Tokens are persistent and don't expire by default
- Each user has one unique token
- Tokens are stored in the `authtoken_token` database table

### Protected Endpoints:

By default, all API endpoints except registration and login require authentication. This is configured in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

## Configuration

### Key Settings in `settings.py`

```python
# Custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Installed apps
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'accounts',
]

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

## Next Steps

Potential enhancements for the API:

- Implement password reset functionality
- Add email verification
- Implement follow/unfollow functionality
- Add user search
- Implement posts and comments
- Add likes and shares
- Implement notifications
- Add pagination for list views
- Implement rate limiting
- Add API documentation with Swagger/OpenAPI

## License

This project is created for educational purposes.

## Support

For issues or questions, please contact the development team or create an issue in the project repository.
