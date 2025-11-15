# Quick Reference: Testing Permissions System

## Initial Setup

### 1. Run Migrations
```bash
cd LibraryProject
python manage.py migrate
```

### 2. Create Groups and Permissions
```bash
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings'); import django; django.setup(); exec(open('setup_groups_permissions.py').read())"
```

### 3. Verify Groups Were Created
```bash
python manage.py shell
>>> from django.contrib.auth.models import Group
>>> groups = Group.objects.all()
>>> for group in groups:
...     print(f"{group.name}: {group.permissions.count()} permissions")
```

Expected output:
```
Viewers: 1 permissions
Editors: 4 permissions
Admins: 6 permissions
```

## Creating Test Users

In Django shell (`python manage.py shell`):

```python
from bookshelf.models import CustomUser
from django.contrib.auth.models import Group

# Create Viewer user
viewer = CustomUser.objects.create_user(
    username='viewer_test',
    password='testpass123',
    email='viewer@test.com'
)
viewer.groups.add(Group.objects.get(name='Viewers'))
print("Created viewer_test user in Viewers group")

# Create Editor user
editor = CustomUser.objects.create_user(
    username='editor_test',
    password='testpass123',
    email='editor@test.com'
)
editor.groups.add(Group.objects.get(name='Editors'))
print("Created editor_test user in Editors group")

# Create Admin user
admin_user = CustomUser.objects.create_user(
    username='admin_test',
    password='testpass123',
    email='admin@test.com'
)
admin_user.groups.add(Group.objects.get(name='Admins'))
print("Created admin_test user in Admins group")
```

## Running Tests

### Automated Permission Tests
```bash
cd c:\Users\Yvonne\Alx_DjangoLearnLab\advanced_features_and_security
python permissions_test.py
```

### Manual Permission Tests

#### Start the Django Development Server
```bash
cd LibraryProject
python manage.py runserver
```

Then navigate to: `http://localhost:8000`

#### Test Viewer Access
1. Login as: `viewer_test` / `testpass123`
2. **Can do:**
   - Navigate to `/relationship_app/books/` - ✓ Works
3. **Cannot do:**
   - Navigate to `/relationship_app/books/add/` - ✗ Returns 403 Forbidden
   - Navigate to `/relationship_app/books/1/edit/` - ✗ Returns 403 Forbidden
   - Navigate to `/relationship_app/books/1/delete/` - ✗ Returns 403 Forbidden

#### Test Editor Access
1. Login as: `editor_test` / `testpass123`
2. **Can do:**
   - Navigate to `/relationship_app/books/` - ✓ Works
   - Navigate to `/relationship_app/books/add/` - ✓ Works (can create books)
   - Navigate to `/relationship_app/books/1/edit/` - ✓ Works (can edit books)
3. **Cannot do:**
   - Navigate to `/relationship_app/books/1/delete/` - ✗ Returns 403 Forbidden

#### Test Admin Access
1. Login as: `admin_test` / `testpass123`
2. **Can do:**
   - Navigate to `/relationship_app/books/` - ✓ Works
   - Navigate to `/relationship_app/books/add/` - ✓ Works
   - Navigate to `/relationship_app/books/1/edit/` - ✓ Works
   - Navigate to `/relationship_app/books/1/delete/` - ✓ Works (can delete books)

#### Test Unauthenticated Access
1. Logout or use an incognito window
2. **Result:**
   - All protected pages redirect to login page
   - `/relationship_app/books/` - Redirects to login
   - `/relationship_app/books/add/` - Redirects to login

## Checking User Permissions

In Django shell:

```python
from django.contrib.auth.models import Permission
from bookshelf.models import CustomUser

# Check specific user's permissions
user = CustomUser.objects.get(username='editor_test')

# Get permissions through groups
group_perms = Permission.objects.filter(group__user=user).distinct()

print("Permissions for editor_test:")
for perm in group_perms:
    print(f"  - {perm.codename}: {perm.name}")
```

Expected output:
```
Permissions for editor_test:
  - can_view_book: Can view book
  - can_create_book: Can create book
  - can_edit_book: Can edit book
  - can_manage_authors: Can manage authors
```

## Understanding Permission Decorators

### View Permission Decorator
Each protected view uses Django's `@permission_required` decorator:

```python
@permission_required('relationship_app.can_create_book', raise_exception=True)
def add_book(request):
    # Code here only runs if user has can_create_book permission
    # If user lacks permission, returns HTTP 403 Forbidden
```

### How It Works
1. User sends request to `/relationship_app/books/add/`
2. Django checks if user is authenticated
3. If not authenticated: Redirect to login
4. If authenticated: Check if user has `can_create_book` permission
5. If has permission: Allow access to view
6. If no permission: Return HTTP 403 Forbidden

## Troubleshooting

### Issue: Users can't access protected views
**Solution:** Make sure users are in the correct groups:
```python
from bookshelf.models import CustomUser
from django.contrib.auth.models import Group

user = CustomUser.objects.get(username='username')
print("Groups:", list(user.groups.all()))

# Add to group if needed
editors_group = Group.objects.get(name='Editors')
user.groups.add(editors_group)
```

### Issue: Migrations haven't been applied
**Solution:** Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Groups don't exist
**Solution:** Run the setup script:
```bash
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings'); import django; django.setup(); exec(open('setup_groups_permissions.py').read())"
```

### Issue: See "Permission matching query does not exist" error
**Solution:** This means the permission objects haven't been created in database. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `LibraryProject/relationship_app/models.py` | Defines custom permissions in Book Meta class |
| `LibraryProject/relationship_app/views.py` | Uses @permission_required decorators on views |
| `LibraryProject/setup_groups_permissions.py` | Script to create groups and assign permissions |
| `PERMISSIONS_GUIDE.md` | Comprehensive documentation |
| `permissions_test.py` | Automated test suite |

## Permission Matrix Reference

### Custom Permissions
- `can_view_book` - Required to view/list books
- `can_create_book` - Required to create new books
- `can_edit_book` - Required to edit existing books
- `can_delete_book` - Required to delete books
- `can_publish_book` - Reserved for future publishing feature
- `can_manage_authors` - Required to manage author relationships

### Default Groups

**Viewers** - Read-only members
- Permissions: can_view_book

**Editors** - Content managers
- Permissions: can_view_book, can_create_book, can_edit_book, can_manage_authors

**Admins** - Full administrators
- Permissions: All 6 permissions

## Database Queries for Permissions

```python
# Get all permissions
from django.contrib.auth.models import Permission
all_perms = Permission.objects.filter(content_type__app_label='relationship_app')

# Get specific permission
from django.contrib.auth.models import Permission
can_view = Permission.objects.get(codename='can_view_book')

# Get users with specific permission
users_with_view = User.objects.filter(groups__permissions__codename='can_view_book').distinct()

# Get all users in a group
from django.contrib.auth.models import Group
editors_users = Group.objects.get(name='Editors').user_set.all()

# Check if user has permission
user = User.objects.get(username='john')
has_permission = user.has_perm('relationship_app.can_create_book')
```

## Additional Resources

- Django Permissions Docs: https://docs.djangoproject.com/en/stable/topics/auth/
- PERMISSIONS_GUIDE.md - Complete documentation
- permissions_test.py - Automated verification
