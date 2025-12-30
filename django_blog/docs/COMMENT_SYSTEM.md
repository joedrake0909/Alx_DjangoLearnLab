# Comment Functionality Documentation

## Overview
This document describes the complete comment system implementation for the Django blog project, allowing users to engage with blog posts through comments.

---

## Features Implemented

### Comment System Capabilities
- ✅ **View Comments**: All users can see comments on blog posts
- ✅ **Add Comments**: Authenticated users can post comments on any blog post
- ✅ **Edit Comments**: Users can edit their own comments
- ✅ **Delete Comments**: Users can delete their own comments
- ✅ **Timestamps**: Comments show creation time and edit status
- ✅ **Author Protection**: Only comment authors can modify/delete their comments

---

## Database Schema

### Comment Model
Located in: `blog/models.py`

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
```

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `post` | ForeignKey | Links comment to specific blog post (many-to-one) |
| `author` | ForeignKey | User who wrote the comment |
| `content` | TextField | The actual comment text |
| `created_at` | DateTimeField | Automatically set when comment is created |
| `updated_at` | DateTimeField | Automatically updated on each save |

**Relationships:**
- One Post → Many Comments
- One User → Many Comments
- Comments deleted when post is deleted (CASCADE)
- Comments deleted when user is deleted (CASCADE)

**Meta Options:**
- `ordering = ['created_at']` - Comments display oldest first

---

## Forms

### CommentForm
Located in: `blog/forms.py`

```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }
```

**Features:**
- Only includes `content` field (post and author set automatically)
- Custom textarea with 4 rows and placeholder text
- Built-in validation from TextField requirements

---

## Views

### Comment CRUD Operations

#### 1. Add Comment (Function-Based View)
**Function:** `add_comment(request, pk)`
**URL:** `/post/<int:pk>/comments/new/`
**Method:** POST/GET
**Permission:** LoginRequired

```python
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})
```

**How it works:**
1. Gets the post by ID (404 if not found)
2. If POST: validates form, sets post and author automatically, saves
3. If GET: displays empty form
4. Redirects to post detail page after successful save
5. Shows success message

#### 2. Update Comment (Class-Based View)
**Class:** `CommentUpdateView`
**URL:** `/comment/<int:pk>/update/`
**Permission:** LoginRequired + Author Only

```python
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your comment has been updated!')
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
```

**Security:**
- `LoginRequiredMixin`: Must be logged in
- `UserPassesTestMixin`: Must be comment author
- `test_func()`: Returns True only if user is author
- Non-authors get 403 Forbidden error

**Flow:**
1. Loads existing comment data into form
2. User edits content
3. Validates and saves changes
4. Updates `updated_at` timestamp automatically
5. Redirects back to post detail page

#### 3. Delete Comment (Class-Based View)
**Class:** `CommentDeleteView`
**URL:** `/comment/<int:pk>/delete/`
**Permission:** LoginRequired + Author Only

```python
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        messages.success(self.request, 'Your comment has been deleted!')
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
```

**Flow:**
1. Shows confirmation page with comment preview
2. User confirms deletion
3. Deletes comment from database
4. Shows success message
5. Redirects to post detail page

---

## URL Patterns

Located in: `blog/urls.py`

```python
# Comment URLs
path('post/<int:pk>/comments/new/', views.add_comment, name='add-comment'),
path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
```

**URL Structure:**

| Action | URL Pattern | View | Name |
|--------|-------------|------|------|
| Add | `/post/<post_id>/comments/new/` | add_comment | add-comment |
| Edit | `/comment/<comment_id>/update/` | CommentUpdateView | comment-update |
| Delete | `/comment/<comment_id>/delete/` | CommentDeleteView | comment-delete |

**Examples:**
- Add comment to post #5: `/post/5/comments/new/`
- Edit comment #12: `/comment/12/update/`
- Delete comment #12: `/comment/12/delete/`

---

## Templates

### 1. Post Detail Template (blog/post_detail.html)
**Displays:** Comments list integrated into post view

**Features:**
- Shows comment count: `{{ post.comments.count }}`
- Lists all comments with author, date, content
- Shows "(edited)" tag if comment was updated
- "Add Comment" button for logged-in users
- Edit/Delete buttons visible only to comment author
- Login prompt for anonymous users

**Comment Display:**
```html
{% for comment in post.comments.all %}
    <div class="comment">
        <div class="comment-header">
            <strong>{{ comment.author.username }}</strong>
            <span>{{ comment.created_at|date:"F d, Y \a\t g:i A" }}</span>
            {% if comment.created_at != comment.updated_at %}
                (edited)
            {% endif %}
        </div>
        <div class="comment-content">
            <p>{{ comment.content|linebreaks }}</p>
        </div>
        {% if user == comment.author %}
            <a href="{% url 'comment-update' comment.pk %}">Edit</a>
            <a href="{% url 'comment-delete' comment.pk %}">Delete</a>
        {% endif %}
    </div>
{% endfor %}
```

### 2. Add Comment Template (blog/add_comment.html)
**Purpose:** Form to create new comment

**Features:**
- Shows which post you're commenting on
- Comment textarea with placeholder
- Post/Cancel buttons
- CSRF protection

### 3. Edit Comment Template (blog/comment_form.html)
**Purpose:** Form to edit existing comment

**Features:**
- Pre-filled with current comment content
- Shows original post title
- Shows original comment date
- Update/Cancel buttons

### 4. Delete Confirmation Template (blog/comment_confirm_delete.html)
**Purpose:** Confirm before deleting comment

**Features:**
- Shows comment preview (truncated to 50 words)
- Shows post title, author, and date
- Warning message
- Confirm/Cancel buttons

---

## Permissions & Security

### Access Control Matrix

| Action | Anonymous | Authenticated | Comment Author | Other Users |
|--------|-----------|---------------|----------------|-------------|
| View Comments | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Add Comment | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| Edit Comment | ❌ No | ❌ No | ✅ Yes | ❌ No (403) |
| Delete Comment | ❌ No | ❌ No | ✅ Yes | ❌ No (403) |

### Security Measures

1. **Authentication Required:**
   - `@login_required` decorator on add_comment view
   - `LoginRequiredMixin` on edit/delete views
   - Redirects to login page if not authenticated

2. **Authorization Checks:**
   - `UserPassesTestMixin` ensures only author can edit/delete
   - `test_func()` compares `request.user` with `comment.author`
   - Returns 403 Forbidden if unauthorized

3. **CSRF Protection:**
   - All forms include `{% csrf_token %}`
   - Django validates token on POST requests

4. **Automatic Field Assignment:**
   - Author set to `request.user` (not user-editable)
   - Post set from URL parameter (not user-editable)
   - Prevents impersonation or comment hijacking

---

## Usage Guide

### For End Users

#### Viewing Comments
1. Navigate to any blog post detail page
2. Scroll down to see comments section
3. Comments appear oldest-first
4. Each comment shows author, date, and content

#### Adding a Comment
1. Go to a blog post detail page
2. Click "Add Comment" button (must be logged in)
3. Type your comment in the textarea
4. Click "Post Comment"
5. Redirected back to post with success message
6. Your comment appears at the bottom

#### Editing Your Comment
1. Find your comment on a post
2. Click "Edit" button (only visible for your comments)
3. Modify the text
4. Click "Update Comment"
5. Comment shows "(edited)" tag next to date

#### Deleting Your Comment
1. Find your comment on a post
2. Click "Delete" button
3. Confirm deletion on warning page
4. Comment removed permanently

### For Developers

#### Creating Migrations
After adding the Comment model, run:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Admin Access
Comment model registered in admin:
```python
admin.site.register(Comment)
```
Access at: `/admin/blog/comment/`

#### Testing Permissions
```python
# Test 1: Anonymous users redirected to login
response = client.get('/post/1/comments/new/')
assert response.status_code == 302  # Redirect to login

# Test 2: Only author can edit
comment = Comment.objects.get(pk=1)
client.login(username='otheruser')
response = client.get(f'/comment/{comment.pk}/update/')
assert response.status_code == 403  # Forbidden
```

---

## Database Queries

### Get all comments for a post:
```python
post = Post.objects.get(pk=1)
comments = post.comments.all()  # Uses related_name='comments'
```

### Get comment count:
```python
count = post.comments.count()
```

### Get user's comments:
```python
user_comments = Comment.objects.filter(author=request.user)
```

### Get recent comments:
```python
recent = Comment.objects.order_by('-created_at')[:10]
```

---

## Features & Functionality

### Automatic Timestamps
- `created_at`: Set once when comment is created (auto_now_add=True)
- `updated_at`: Updates every time comment is saved (auto_now=True)
- Template shows "(edited)" if timestamps differ

### Related Name
- `related_name='comments'` on ForeignKey
- Allows `post.comments.all()` instead of `post.comment_set.all()`
- Cleaner, more intuitive code

### Ordering
- `Meta: ordering = ['created_at']`
- Comments always display oldest-first
- Consistent chronological conversation flow

### Success Messages
- Django messages framework provides feedback
- "Your comment has been added!"
- "Your comment has been updated!"
- "Your comment has been deleted!"

---

## Testing Checklist

### Functionality Tests
- [ ] Anonymous users can view comments
- [ ] Anonymous users cannot add comments (redirected to login)
- [ ] Logged-in users can add comments
- [ ] Comment appears immediately after posting
- [ ] Authors can edit their own comments
- [ ] Authors can delete their own comments
- [ ] Non-authors cannot edit others' comments (403)
- [ ] Non-authors cannot delete others' comments (403)
- [ ] Edited comments show "(edited)" tag
- [ ] Deleting comment redirects to post page
- [ ] Deleting post deletes all its comments

### Edge Cases
- [ ] Empty comment rejected (validation)
- [ ] Very long comment displays correctly
- [ ] Comment on non-existent post returns 404
- [ ] Editing non-existent comment returns 404
- [ ] Multiple comments by same user allowed
- [ ] Comment count updates correctly

---

## Troubleshooting

### Issue: "RelatedObjectDoesNotExist" error
**Solution:** Run migrations to create Comment table:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Can't see "Add Comment" button
**Solution:** You must be logged in. Click "Login" in navigation.

### Issue: 403 Forbidden when editing comment
**Solution:** You can only edit your own comments. Make sure you're logged in as the comment author.

### Issue: Comments not appearing
**Solution:** Check that:
1. Comments exist in database
2. Template loop syntax is correct
3. Related name 'comments' is used correctly

---

## File Structure

```
django_blog/
├── blog/
│   ├── models.py                 # Comment model
│   ├── forms.py                  # CommentForm
│   ├── views.py                  # Comment CRUD views
│   ├── urls.py                   # Comment URL patterns
│   ├── admin.py                  # Comment admin registration
│   └── templates/
│       └── blog/
│           ├── post_detail.html          # Shows comments
│           ├── add_comment.html          # Add comment form
│           ├── comment_form.html         # Edit comment form
│           └── comment_confirm_delete.html  # Delete confirmation
```

---

## API Reference

### Model Methods

**Comment.__str__()**
```python
return f'Comment by {self.author.username} on {self.post.title}'
```
Returns: "Comment by john on My Blog Post"

### View Methods

**add_comment(request, pk)**
- Parameters: request (HttpRequest), pk (int - post ID)
- Returns: HttpResponse
- Raises: Http404 if post not found

**CommentUpdateView.test_func()**
- Returns: bool (True if user is comment author)

**CommentDeleteView.get_success_url()**
- Returns: str (URL to post detail page)

---

## Best Practices

### Security
1. Always use `@login_required` for mutating operations
2. Always check ownership with `UserPassesTestMixin`
3. Never expose author field in forms (set automatically)
4. Use `get_object_or_404()` to prevent information disclosure

### Performance
1. Use `select_related('author')` when querying comments
2. Use `prefetch_related('comments')` when loading posts with comments
3. Consider pagination for posts with many comments

### User Experience
1. Show comment count to indicate activity
2. Display author and timestamp for context
3. Provide clear edit/delete buttons for authors only
4. Show success messages for all actions
5. Use confirmation page before deletion

---

## Future Enhancements

Potential features to add:

1. **Nested Comments** - Reply to specific comments
2. **Likes/Votes** - Upvote/downvote comments
3. **Moderation** - Flag inappropriate comments
4. **Notifications** - Email authors when their posts get comments
5. **Rich Text** - Markdown or WYSIWYG editor
6. **Comment Pagination** - Limit comments per page
7. **Sort Options** - Sort by newest/oldest/most liked
8. **User Mentions** - @username tagging
9. **Comment Search** - Search within comments
10. **Anti-Spam** - CAPTCHA or rate limiting

---

## Summary

The comment system is fully functional with:
- Complete CRUD operations
- Proper authentication and authorization
- User-friendly templates
- Security best practices
- Comprehensive error handling

Users can now engage in discussions on blog posts while maintaining data integrity and security.

---

## Quick Reference

**Add Comment:**
```
URL: /post/<post_id>/comments/new/
Permission: Authenticated users
```

**Edit Comment:**
```
URL: /comment/<comment_id>/update/
Permission: Comment author only
```

**Delete Comment:**
```
URL: /comment/<comment_id>/delete/
Permission: Comment author only
```

**View Comments:**
```
Location: On post detail page
Permission: Everyone
```
