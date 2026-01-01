# Quick Start Guide - Social Media API

## ✅ Completed Setup

Your Social Media API is now fully configured with:

1. ✅ Django 5.2.8 installed
2. ✅ Django REST Framework 3.16.1 installed
3. ✅ Custom User model with bio, profile_picture, and followers
4. ✅ Token-based authentication configured
5. ✅ User registration, login, and profile management endpoints
6. ✅ Database migrations applied
7. ✅ Admin panel configured
8. ✅ Complete documentation in README.md

## 🚀 Quick Start

### 1. Start the Development Server

```bash
cd "c:\Users\X1 Carbon\Desktop\Alx_DjangoLearnLab\social_media_api\social_media_api"
python manage.py runserver
```

Server will be available at: **http://127.0.0.1:8000/**

### 2. Access the Admin Panel

First, create a superuser:
```bash
python manage.py createsuperuser
```

Then visit: **http://127.0.0.1:8000/admin/**

### 3. Test the API Endpoints

#### Available Endpoints:
- **POST** `/api/accounts/register/` - Register new user
- **POST** `/api/accounts/login/` - Login and get token
- **GET** `/api/accounts/profile/` - Get user profile (requires token)
- **PUT/PATCH** `/api/accounts/profile/` - Update profile (requires token)

#### Quick Test with cURL:

**Register:**
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"john\",\"email\":\"john@example.com\",\"password\":\"pass123\",\"password_confirm\":\"pass123\"}"
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"john\",\"password\":\"pass123\"}"
```

**Get Profile (replace YOUR_TOKEN):**
```bash
curl -X GET http://127.0.0.1:8000/api/accounts/profile/ ^
  -H "Authorization: Token YOUR_TOKEN"
```

#### Using the Test Script:

```bash
# Install requests library if not already installed
pip install requests

# Run the test script
python test_api.py
```

## 📁 Project Structure

```
social_media_api/
├── manage.py                      # Django management script
├── requirements.txt               # Project dependencies
├── README.md                      # Full documentation
├── test_api.py                   # API testing script
├── db.sqlite3                    # SQLite database
│
├── accounts/                      # User authentication app
│   ├── models.py                 # CustomUser model
│   ├── views.py                  # API views
│   ├── serializers.py            # DRF serializers
│   ├── urls.py                   # App URL routing
│   ├── admin.py                  # Admin configuration
│   └── migrations/               # Database migrations
│       └── 0001_initial.py
│
└── social_media_api/             # Project settings
    ├── settings.py               # Django settings
    ├── urls.py                   # Main URL routing
    ├── wsgi.py                   # WSGI config
    └── asgi.py                   # ASGI config
```

## 🔑 Key Features Implemented

### Custom User Model (`accounts/models.py`)
- Extends Django's AbstractUser
- Additional fields: `bio`, `profile_picture`, `followers`
- Many-to-Many self-relationship for social features

### API Views (`accounts/views.py`)
- **UserRegistrationView**: Creates new users with automatic token generation
- **UserLoginView**: Authenticates users and returns tokens
- **UserProfileView**: Retrieves and updates user profiles

### Serializers (`accounts/serializers.py`)
- **UserRegistrationSerializer**: Handles registration with password confirmation
- **UserLoginSerializer**: Validates login credentials
- **UserProfileSerializer**: Formats user data with follower counts

### Authentication
- Token-based authentication (Django REST Framework)
- Automatic token creation on registration
- Secure password hashing
- Token required for protected endpoints

## 📝 Common Commands

```bash
# Make migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run tests
python manage.py test accounts

# Open Python shell with Django context
python manage.py shell
```

## 🧪 Testing with Postman

1. **Import Collection**: Create a new collection in Postman

2. **Register User**:
   - Method: POST
   - URL: `http://127.0.0.1:8000/api/accounts/register/`
   - Body (raw JSON):
     ```json
     {
         "username": "testuser",
         "email": "test@example.com",
         "password": "testpass123",
         "password_confirm": "testpass123",
         "bio": "Hello World"
     }
     ```

3. **Login**:
   - Method: POST
   - URL: `http://127.0.0.1:8000/api/accounts/login/`
   - Body (raw JSON):
     ```json
     {
         "username": "testuser",
         "password": "testpass123"
     }
     ```
   - Save the token from response

4. **Get Profile**:
   - Method: GET
   - URL: `http://127.0.0.1:8000/api/accounts/profile/`
   - Headers: `Authorization: Token <your-token>`

5. **Update Profile**:
   - Method: PATCH
   - URL: `http://127.0.0.1:8000/api/accounts/profile/`
   - Headers: `Authorization: Token <your-token>`
   - Body (raw JSON):
     ```json
     {
         "bio": "Updated bio text"
     }
     ```

## 🔐 Settings Configuration

Key settings in `social_media_api/settings.py`:

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

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

## 📚 Next Steps

Consider implementing:
- [ ] Password reset functionality
- [ ] Email verification
- [ ] Follow/unfollow users
- [ ] User search
- [ ] Posts and comments
- [ ] Likes and shares
- [ ] Notifications
- [ ] Pagination
- [ ] Rate limiting
- [ ] API documentation (Swagger)

## 🆘 Troubleshooting

**Server won't start:**
- Make sure you're in the correct directory
- Check that migrations are applied: `python manage.py migrate`
- Verify Django is installed: `pip install django djangorestframework`

**Can't create users:**
- Check database migrations are up to date
- Verify INSTALLED_APPS includes 'accounts' and 'rest_framework.authtoken'

**Authentication not working:**
- Ensure you're including the token in the Authorization header
- Format: `Authorization: Token <your-token>`
- Check that the token exists in the database

**Import errors:**
- Install required packages: `pip install -r requirements.txt`

## 📄 Full Documentation

See [README.md](README.md) for comprehensive documentation including:
- Detailed API endpoint descriptions
- Complete request/response examples
- User model field descriptions
- Advanced configuration options
- Security best practices

---

**Project Status**: ✅ Ready for Development and Testing

**Last Updated**: January 1, 2026
