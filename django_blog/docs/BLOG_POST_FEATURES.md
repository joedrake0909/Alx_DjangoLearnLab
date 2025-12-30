# Blog Post Management Features

## Overview
This Django blog project implements full CRUD (Create, Read, Update, Delete) operations for blog posts with proper authentication and authorization controls.

## Features Implemented

### 1. **CRUD Operations**

#### List Posts (Read All)
- **URL**: `/` or `/posts/`
- **View**: `PostListView` (ListView)
- **Template**: `post_list.html`
- **Access**: Public (all users)
- **Features**:
  - Displays all blog posts ordered by newest first
  - Shows post title, author, date, and content preview (first 50 words)
  - Pagination (5 posts per page)
  - "Create New Post" button for authenticated users

#### View Post Details (Read One)
- **URL**: `/posts/<int:pk>/`
- **View**: `PostDetailView` (DetailView)
- **Template**: `post_detail.html`
- **Access**: Public (all users)
- **Features**:
  - Shows complete post with title, author, date, and full content
  - Edit and Delete buttons visible only to the post author
  - Back to list navigation

#### Create New Post
- **URL**: `/posts/new/`
- **View**: `PostCreateView` (CreateView)
- **Template**: `post_form.html`
- **Access**: Authenticated users only (LoginRequiredMixin)
- **Features**:
  - Form with title and content fields
  - Author automatically set to logged-in user
  - Redirects to post detail page after creation

#### Update Post
- **URL**: `/posts/<int:pk>/edit/`
- **View**: `PostUpdateView` (UpdateView)
- **Template**: `post_form.html`
- **Access**: Post author only (LoginRequiredMixin + UserPassesTestMixin)
- **Features**:
  - Pre-filled form with existing post data
  - Only the author can edit their own posts
  - Returns 403 Forbidden if non-author tries to access

#### Delete Post
- **URL**: `/posts/<int:pk>/delete/`
- **View**: `PostDeleteView` (DeleteView)
- **Template**: `post_confirm_delete.html`
- **Access**: Post author only (LoginRequiredMixin + UserPassesTestMixin)
- **Features**:
  - Confirmation page showing post details
  - Warning about irreversible action
  - Redirects to post list after deletion

---

## Models

### Post Model
Located in: `blog/models.py`

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

**Fields:**
- `title`: Post title (max 200 characters)
- `content`: Full post content (unlimited text)
- `published_date`: Automatically set when post is created
- `author`: Foreign key to User (deletes posts if user is deleted)

**Methods:**
- `__str__()`: Returns post title for admin display
- `get_absolute_url()`: Returns URL to post detail page

---

## Forms

### PostForm
Located in: `blog/forms.py`

```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
```

**Features:**
- ModelForm automatically generates form fields from Post model
- Only includes title and content (author is set automatically)
- Built-in validation from model constraints

---

## Views

### Class-Based Views
Located in: `blog/views.py`

All views use Django's generic class-based views for efficiency:

1. **PostListView**
   - Inherits: `ListView`
   - Orders by: `-published_date` (newest first)
   - Pagination: 5 posts per page

2. **PostDetailView**
   - Inherits: `DetailView`
   - Shows single post with all details

3. **PostCreateView**
   - Inherits: `LoginRequiredMixin`, `CreateView`
   - Sets author to current user in `form_valid()`

4. **PostUpdateView**
   - Inherits: `LoginRequiredMixin`, `UserPassesTestMixin`, `UpdateView`
   - `test_func()` ensures only author can edit

5. **PostDeleteView**
   - Inherits: `LoginRequiredMixin`, `UserPassesTestMixin`, `DeleteView`
   - `test_func()` ensures only author can delete
   - Redirects to post list after deletion

---

## URLs

Located in: `blog/urls.py`

```python
# Blog Post URLs
path('', PostListView.as_view(), name='post-list'),
path('posts/', PostListView.as_view(), name='post-list'),
path('posts/new/', PostCreateView.as_view(), name='post-create'),
path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
```

**URL Patterns:**
- `/` - Homepage (post list)
- `/posts/` - All posts
- `/posts/new/` - Create new post
- `/posts/5/` - View post #5
- `/posts/5/edit/` - Edit post #5
- `/posts/5/delete/` - Delete post #5

---

## Templates

All templates extend `base.html` and are located in `blog/templates/blog/`

### post_list.html
- Lists all blog posts
- Shows post preview (title, author, date, truncated content)
- Pagination controls
- "Create New Post" button for logged-in users

### post_detail.html
- Full post display
- Edit/Delete buttons (visible only to author)
- Back to list link

### post_form.html
- Reusable form for both create and update
- Shows "Create Post" or "Update Post" based on context
- CSRF protection
- Cancel button returns to list

### post_confirm_delete.html
- Delete confirmation page
- Shows post preview
- Warning message
- Confirm/Cancel buttons

---

## Permissions & Security

### Authentication Requirements

1. **Public Access (No login required):**
   - View post list
   - View individual posts

2. **Authenticated Users Only:**
   - Create new posts

3. **Post Author Only:**
   - Edit their own posts
   - Delete their own posts

### Security Features

- **LoginRequiredMixin**: Redirects to login page if user not authenticated
- **UserPassesTestMixin**: Returns 403 Forbidden if user fails permission test
- **CSRF Protection**: All forms include `{% csrf_token %}`
- **Automatic Author Assignment**: Author set programmatically (not in form)

### Permission Checks

```python
def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
```

This ensures only the post author can edit/delete their posts.

---

## Testing Guide

### Test Create Post
1. Register/login as a user
2. Click "New Post" in navigation
3. Fill in title and content
4. Submit form
5. Verify redirect to post detail page
6. Verify post appears in list

### Test Update Post
1. Login as post author
2. View one of your posts
3. Click "Edit Post"
4. Modify title or content
5. Submit form
6. Verify changes appear

### Test Delete Post
1. Login as post author
2. View one of your posts
3. Click "Delete Post"
4. Confirm deletion
5. Verify redirect to post list
6. Verify post no longer appears

### Test Permissions
1. Login as User A
2. Create a post
3. Logout and login as User B
4. Try to access `/posts/1/edit/` (User A's post)
5. Should receive 403 Forbidden error
6. Same for delete: `/posts/1/delete/`

### Test Pagination
1. Create 10+ posts
2. Go to post list
3. Verify only 5 posts per page
4. Test Previous/Next buttons

---

## Code Structure

```
django_blog/
├── blog/
│   ├── models.py          # Post and Profile models
│   ├── views.py           # CRUD class-based views
│   ├── forms.py           # PostForm, UserForms, ProfileForms
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin configuration
│   ├── templates/
│   │   └── blog/
│   │       ├── base.html              # Base template
│   │       ├── post_list.html         # List all posts
│   │       ├── post_detail.html       # Single post view
│   │       ├── post_form.html         # Create/Edit form
│   │       ├── post_confirm_delete.html # Delete confirmation
│   │       ├── register.html
│   │       ├── login.html
│   │       ├── logout.html
│   │       └── profile.html
│   └── static/
│       ├── css/
│       │   └── styles.css
│       └── js/
│           └── scripts.js
└── manage.py
```

---

## Usage Examples

### Creating a Post
1. Navigate to `/posts/new/`
2. User must be logged in (redirected if not)
3. Fill form and submit
4. Post created with current user as author

### Editing a Post
1. Navigate to `/posts/<id>/edit/`
2. Only author can access (403 otherwise)
3. Form pre-filled with current data
4. Submit to save changes

### Deleting a Post
1. Navigate to `/posts/<id>/delete/`
2. Only author can access (403 otherwise)
3. Confirmation page displayed
4. Confirm to permanently delete

---

## Key Implementation Details

### Automatic Author Assignment
```python
def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)
```
This prevents users from changing the author field.

### Author-Only Access Control
```python
def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
```
Returns True only if current user is the post author.

### URL Redirection
```python
def get_absolute_url(self):
    return reverse('post-detail', kwargs={'pk': self.pk})
```
After creating/editing, redirects to the post's detail page.

---

## Navigation Flow

```
Post List → Post Detail → Edit/Delete
    ↓           ↑
Create New ─────┘
```

1. Homepage shows all posts
2. Click post title to view details
3. Author sees Edit/Delete buttons
4. Edit returns to detail page after save
5. Delete returns to list page after confirmation

---

## Success Criteria

✅ **All CRUD operations working**
- Create: PostCreateView with form
- Read: PostListView and PostDetailView
- Update: PostUpdateView with permissions
- Delete: PostDeleteView with confirmation

✅ **Proper permissions implemented**
- Public can view all posts
- Only authenticated users can create
- Only authors can edit/delete their posts

✅ **User-friendly templates**
- Clean, responsive design
- Clear navigation
- Appropriate feedback messages

✅ **Secure implementation**
- CSRF protection on all forms
- Login required for sensitive operations
- Author verification for edit/delete

---

## Next Steps / Future Enhancements

- Add categories/tags for posts
- Implement search functionality
- Add comments system
- Rich text editor for content
- Draft/Published status
- Post view counter
- Social sharing buttons
- RSS feed

---

## Troubleshooting

**Issue: 403 Forbidden when trying to edit**
- Solution: Make sure you're logged in as the post author

**Issue: Can't see "New Post" button**
- Solution: You need to be logged in

**Issue: Posts not showing**
- Solution: Create some posts first using `/posts/new/`

**Issue: Pagination not working**
- Solution: Need 6+ posts to see pagination (5 per page)

---

## Documentation Complete

This blog post management system provides complete CRUD functionality with proper security and user experience considerations. All code follows Django best practices and uses class-based views for maintainability.
