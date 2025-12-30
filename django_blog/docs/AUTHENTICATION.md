# Authentication System Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [User Flow](#user-flow)
4. [Component Details](#component-details)
5. [How to Test](#how-to-test)
6. [Troubleshooting](#troubleshooting)

---

## Overview

The Django blog uses Django's built-in authentication system to manage user accounts. It includes:
- **User Registration** - New users can create accounts
- **User Login** - Existing users can authenticate
- **User Logout** - Users can end their sessions
- **User Profiles** - Authenticated users can view their profile
- **Password Security** - Passwords are hashed and validated

### Key Features
- ✅ Custom registration form with email validation
- ✅ Django's built-in User model for account management
- ✅ Session-based authentication
- ✅ CSRF protection on all forms
- ✅ Protected routes that require login

---

## Architecture

### Components

```
User Authentication System
├── Models
│   └── User (Django built-in)
├── Forms
│   └── CustomUserCreationForm
├── Views
│   ├── register() - Handle registration
│   ├── profile() - Show user profile (protected)
│   ├── LoginView - Handle login (built-in)
│   └── LogoutView - Handle logout (built-in)
├── Templates
│   ├── register.html
│   ├── login.html
│   ├── profile.html
│   └── logout.html
└── URLs
    └── /register/, /login/, /logout/, /profile/
```

### Technology Stack
- **Django Version**: 6.0
- **Database**: PostgreSQL
- **Authentication Method**: Session-based (built-in Django)
- **Password Hashing**: PBKDF2 (Django default)

---

## User Flow

### Registration Flow
```
User visits /register/
    ↓
Fills form (username, email, password, password_confirm)
    ↓
Form validation happens:
    - Username unique?
    - Email valid?
    - Passwords match?
    - Password strength check?
    ↓
If valid:
    - User created in database
    - User automatically logged in
    - Redirect to /profile/
↓
If invalid:
    - Error messages shown
    - Form redisplayed
```

### Login Flow
```
User visits /login/
    ↓
Fills form (username, password)
    ↓
Django verifies credentials:
    - Username exists?
    - Password correct?
    ↓
If valid:
    - Session created
    - User redirected to /profile/ (LOGIN_REDIRECT_URL)
    ↓
If invalid:
    - "Invalid username or password" error
    - Form redisplayed
```

### Profile Access Flow
```
User visits /profile/
    ↓
@login_required decorator checks:
    - Is user authenticated?
    ↓
If yes:
    - Show profile page with user info
    ↓
If no:
    - Redirect to /login/
```

### Logout Flow
```
User clicks logout button
    ↓
Session is destroyed
    ↓
User redirected to logout confirmation page
    ↓
User can click link to go back to login
```

---

## Component Details

### 1. **User Model** (Django Built-in)
**File**: Not in your code (Django's `django.contrib.auth.models`)

**Fields**:
- `username` - Unique identifier for login
- `email` - User's email address
- `password` - Hashed password (never stored as plain text)
- `first_name` - Optional
- `last_name` - Optional
- `is_active` - Whether account is enabled
- `is_staff` - Whether user can access admin
- `is_superuser` - Whether user is admin
- `date_joined` - When account was created
- `last_login` - When user last logged in

**Database Table**: `auth_user`

---

### 2. **CustomUserCreationForm**
**File**: [blog/forms.py](../blog/forms.py)

```python
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email']
```

**What it does**:
- Extends Django's `UserCreationForm`
- Adds `email` field (required)
- Includes built-in password validation:
  - ✅ Minimum 8 characters
  - ✅ Not all numeric
  - ✅ Not similar to username
  - ✅ Not common passwords
- Validates passwords match
- Creates new User object

**Inherited Fields**:
- `password1` - Password entry
- `password2` - Password confirmation

---

### 3. **Register View**
**File**: [blog/views.py](../blog/views.py#L1-L18)

```python
def register(request):
    if request.method == 'POST':
        # User submitted form
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create user in database
            login(request, user)  # Auto-login after registration
            return redirect('profile')  # Go to profile
    else:
        # First visit - show empty form
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})
```

**What happens**:
- GET request: Show registration form
- POST request: Validate and create user
- If valid: Auto-login + redirect to profile
- If invalid: Show form with error messages

**Security Features**:
- ✅ CSRF token in form ({% csrf_token %})
- ✅ Password hashing (form.save() handles this)
- ✅ Email validation
- ✅ Password strength validation

---

### 4. **Login View** (Built-in Django)
**URL**: `/login/` → `LoginView.as_view(template_name='blog/login.html')`

**What Django does automatically**:
- Shows login form
- Validates username/password against database
- Creates session cookie on successful login
- Redirects to `LOGIN_REDIRECT_URL` (set in settings.py)

**Settings** (in [settings.py](../django_blog/settings.py#L92)):
```python
LOGIN_REDIRECT_URL = 'profile'  # Where to go after login
LOGOUT_REDIRECT_URL = 'login'   # Where to go after logout
```

---

### 5. **Logout View** (Built-in Django)
**URL**: `/logout/` → `LogoutView.as_view(template_name='blog/logout.html')`

**What Django does automatically**:
- Destroys session cookie
- Logs user out
- Shows logout confirmation page
- User is redirected to `LOGOUT_REDIRECT_URL`

---

### 6. **Profile View** (Protected)
**File**: [blog/views.py](../blog/views.py#L21-L23)

```python
@login_required
def profile(request):
    return render(request, 'blog/profile.html')
```

**The `@login_required` Decorator**:
- Checks if user is authenticated
- If not authenticated: Redirects to `/login/`
- If authenticated: Allows access to profile page

**Variables available in template**:
- `{{ user.username }}` - Current logged-in user
- `{{ user.email }}` - Their email
- `{{ user.first_name }}` - First name (if set)
- `{{ user.last_name }}` - Last name (if set)
- `{{ user.is_authenticated }}` - Boolean (always True here)

---

### 7. **URL Configuration**
**File**: [blog/urls.py](../blog/urls.py)

```python
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
]
```

**URL Endpoints**:
| URL | Name | View | Purpose |
|-----|------|------|---------|
| `/register/` | register | Custom view | New user signup |
| `/login/` | login | Django built-in | User authentication |
| `/profile/` | profile | Custom view (protected) | Show user info |
| `/logout/` | logout | Django built-in | End session |

---

## How to Test

### Prerequisites
1. Start Django development server:
```bash
python manage.py runserver
```
2. Open browser: `http://localhost:8000`

---

### Test 1: User Registration

**Test Case: Successful Registration**
1. Go to `/register/`
2. Fill form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `SecurePass123!`
   - Confirm Password: `SecurePass123!`
3. Click "Sign Up"
4. **Expected**: 
   - ✅ Redirected to `/profile/`
   - ✅ See "Your Profile" with username and email
   - ✅ User appears in Django admin

**Test Case: Password Mismatch**
1. Go to `/register/`
2. Enter:
   - Password: `SecurePass123!`
   - Confirm Password: `Different123!`
3. Click "Sign Up"
4. **Expected**: 
   - ❌ Form shows error: "Passwords don't match"
   - ❌ User NOT created

**Test Case: Weak Password**
1. Go to `/register/`
2. Try password: `123456` (too weak)
3. **Expected**: 
   - ❌ Error: "Too short or too common"
   - ❌ User NOT created

**Test Case: Duplicate Username**
1. Register `testuser2`
2. Try to register again with same username
3. **Expected**: 
   - ❌ Error: "Username already exists"
   - ❌ User NOT created

**Test Case: Missing Email**
1. Leave email field empty
2. Try to submit
3. **Expected**: 
   - ❌ Error: "Email is required"
   - ❌ Form not submitted

**Test Case: Invalid Email**
1. Email: `notanemail`
2. Try to submit
3. **Expected**: 
   - ❌ Error: "Invalid email format"
   - ❌ User NOT created

---

### Test 2: User Login

**Prerequisites**: Create a test user first (register or use Django admin)

**Test Case: Successful Login**
1. Logout if already logged in
2. Go to `/login/`
3. Enter:
   - Username: `testuser`
   - Password: `SecurePass123!`
4. Click "Login"
5. **Expected**: 
   - ✅ Redirected to `/profile/`
   - ✅ See your profile information

**Test Case: Wrong Password**
1. Go to `/login/`
2. Enter:
   - Username: `testuser`
   - Password: `WrongPassword!`
3. Click "Login"
4. **Expected**: 
   - ❌ Error: "Invalid username or password"
   - ❌ Stay on login page
   - ❌ NOT logged in

**Test Case: Non-existent Username**
1. Go to `/login/`
2. Enter:
   - Username: `nonexistent`
   - Password: `SomePass123!`
3. Click "Login"
4. **Expected**: 
   - ❌ Error: "Invalid username or password"
   - ❌ Stay on login page

**Test Case: Case Sensitivity**
1. Go to `/login/`
2. Enter:
   - Username: `TESTUSER` (uppercase)
   - Password: `SecurePass123!`
3. **Expected**: 
   - ❌ Should fail (usernames are case-sensitive)

---

### Test 3: Protected Profile Access

**Test Case: Access Profile While Logged In**
1. Login as `testuser`
2. Go to `/profile/`
3. **Expected**: 
   - ✅ See profile page with user information
   - ✅ Can see username and email

**Test Case: Access Profile While Logged Out**
1. Logout
2. Go to `/profile/`
3. **Expected**: 
   - ❌ Redirected to `/login/`
   - ❌ See login form
   - ❌ Get redirected back to `/profile/` after login

**Test Case: Direct URL Access When Logged Out**
1. Paste in browser: `http://localhost:8000/profile/`
2. **Expected**: 
   - ❌ Redirected to `/login/`

---

### Test 4: Logout

**Test Case: Successful Logout**
1. Login as `testuser`
2. Go to `/logout/`
3. **Expected**: 
   - ✅ See logout confirmation page
   - ✅ Session destroyed (can't access `/profile/` without login)

**Test Case: Verify Session Destroyed**
1. Logout
2. Try to go to `/profile/`
3. **Expected**: 
   - ❌ Redirected to `/login/`
   - ❌ Session cookie deleted

---

### Test 5: Session & Cookies

**Test Case: Verify Session Cookie Created**
1. Open browser DevTools (F12)
2. Go to "Application" → "Cookies" → `localhost:8000`
3. Login
4. **Expected**: 
   - ✅ New cookie appears: `sessionid`
   - ✅ Cookie has expiration time

**Test Case: Verify Session Destroyed After Logout**
1. While logged in, note the `sessionid` cookie
2. Logout
3. **Expected**: 
   - ✅ `sessionid` cookie is gone
   - ❌ Session no longer valid in database

---

### Test 6: CSRF Protection

**Test Case: CSRF Token Present**
1. Go to `/register/` or `/login/`
2. Inspect HTML (right-click → Inspect)
3. Look for form
4. **Expected**: 
   - ✅ See `<input type="hidden" name="csrftoken" value="..."/>`
   - ✅ This prevents CSRF attacks

---

### Test 7: Integration Testing

**Test Case: Complete User Journey**
1. Start fresh (logout if needed)
2. Click "Register here" link from login page
3. Register new user `john_doe` with email
4. Land on profile page
5. Logout
6. Login with same credentials
7. See profile again
8. Logout
9. Try to access profile (should redirect to login)
10. **Expected**: 
   - ✅ All steps work smoothly
   - ✅ No errors

---

## Troubleshooting

### Problem: "Template Does Not Exist"
**Error**: `TemplateDoesNotExist: blog/login.html`

**Cause**: Template files missing or in wrong location

**Solution**:
- Ensure templates are in `blog/templates/blog/` directory
- Check spelling matches exactly
- Run `python manage.py check`

---

### Problem: "No Such Table: auth_user"
**Error**: `ProgrammingError: relation "public.auth_user" does not exist`

**Cause**: Migrations not applied

**Solution**:
```bash
python manage.py migrate
```

---

### Problem: Password Validation Too Strict
**Error**: "Password is too similar to username"

**Cause**: Django's default validators

**Solution**: 
- Choose password different from username
- Or customize validators in `settings.py`

---

### Problem: "Login Required" Redirects to Wrong Page
**Issue**: After login, not redirected to `/profile/`

**Solution**: Check [settings.py](../django_blog/settings.py#L92):
```python
LOGIN_REDIRECT_URL = 'profile'  # URL name, not path
```
Ensure this matches your URL name in `urls.py`

---

### Problem: User Can't Login After Registration
**Cause**: User inactive or password not hashed properly

**Solution**:
1. Check user in Django admin: `http://localhost:8000/admin/`
2. Verify `is_active` is checked
3. Try resetting password

---

### Problem: CSRF Token Errors
**Error**: `Forbidden (403) CSRF verification failed`

**Cause**: Missing `{% csrf_token %}` in form

**Solution**: 
- Ensure template has: `{% csrf_token %}` inside `<form>`
- Check [register.html](../blog/templates/blog/register.html) and [login.html](../blog/templates/blog/login.html)

---

### Problem: Database Connection Error
**Error**: `could not connect to server: Connection refused`

**Cause**: PostgreSQL not running or wrong credentials

**Solution**:
1. Start PostgreSQL service (Windows):
   ```bash
   pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start
   ```
2. Verify credentials in [settings.py](../django_blog/settings.py#L66-L72)
3. Ensure database `django_blog` exists

---

## Security Checklist

- ✅ Passwords are hashed (PBKDF2 by default)
- ✅ CSRF tokens protect against attacks
- ✅ Email validation prevents invalid addresses
- ✅ Password strength requirements enforced
- ✅ `@login_required` protects sensitive views
- ✅ Sessions timeout after browser close (by default)

---

## Advanced Topics (Future Improvements)

### Possible Enhancements
1. **Email Verification**: Send confirmation email on registration
2. **Password Reset**: Forgot password functionality
3. **Two-Factor Authentication**: Additional security layer
4. **Social Login**: Google/GitHub authentication
5. **User Roles**: Permissions and groups
6. **Account Settings**: Edit profile, change password
7. **Email Notifications**: Alert on login from new location
8. **Session Timeout**: Auto-logout after inactivity

---

## References

- [Django Authentication Documentation](https://docs.djangoproject.com/en/6.0/topics/auth/)
- [Django User Model](https://docs.djangoproject.com/en/6.0/ref/contrib/auth/#user-model)
- [Django Forms](https://docs.djangoproject.com/en/6.0/topics/forms/)
- [CSRF Protection](https://docs.djangoproject.com/en/6.0/ref/csrf/)

---

**Last Updated**: December 27, 2025  
**Django Version**: 6.0  
**Database**: PostgreSQL
