# Django Permissions and Groups Management Guide

## Overview

This guide covers the implementation of role-based access control (RBAC) in the Library application using Django's built-in permission and group system. The system enforces granular permissions on book management operations.

## Table of Contents

1. [Custom Permissions](#custom-permissions)
2. [Groups and Their Roles](#groups-and-their-roles)
3. [Group Permission Matrix](#group-permission-matrix)
4. [Setting Up Groups](#setting-up-groups)
5. [Managing Users and Groups](#managing-users-and-groups)
6. [Testing Permissions](#testing-permissions)
7. [Admin Panel Management](#admin-panel-management)

## Custom Permissions

The Book model defines six custom permissions that control specific operations:

| Permission Code | Display Name | Purpose |
|---|---|---|
| `can_view_book` | Can view book | Allows users to view and list books |
| `can_create_book` | Can create book | Allows users to create new books |
| `can_edit_book` | Can edit book | Allows users to modify existing books |
| `can_delete_book` | Can delete book | Allows users to delete books |
| `can_publish_book` | Can publish book | Allows users to publish books (future feature) |
| `can_manage_authors` | Can manage authors | Allows users to manage author relationships |

### How Permissions Work

- Permissions are linked to the Book model in `relationship_app/models.py`
- They are stored in the database and synced with migrations
- Permissions are assigned to groups
- Users inherit permissions through group membership

## Groups and Their Roles

Three default groups are created to manage different access levels:

### 1. Viewers Group
**Read-only access to library content**

- Purpose: Users who can only view books
- Use case: Library members, guests
- Permissions:
  - `can_view_book` - View and list all books

### 2. Editors Group
**Create and modify book records**

- Purpose: Library staff who manage book inventory
- Use case: Librarians, content managers
- Permissions:
  - `can_view_book` - View and list all books
  - `can_create_book` - Add new books to library
  - `can_edit_book` - Modify existing book information
  - `can_manage_authors` - Manage author information

### 3. Admins Group
**Full administrative control**

- Purpose: System administrators with complete control
- Use case: Library administrators, system managers
- Permissions:
  - `can_view_book` - View and list all books
  - `can_create_book` - Add new books to library
  - `can_edit_book` - Modify existing book information
  - `can_delete_book` - Remove books from library
  - `can_publish_book` - Publish books to catalog
  - `can_manage_authors` - Manage author information

## Group Permission Matrix

```
                    | Viewers | Editors | Admins
--------------------|---------|---------|--------
View Books          |    ✓    |    ✓    |   ✓
Create Books        |         |    ✓    |   ✓
Edit Books          |         |    ✓    |   ✓
Delete Books        |         |         |   ✓
Publish Books       |         |         |   ✓
Manage Authors      |         |    ✓    |   ✓
```

## Setting Up Groups

### Initial Setup

Run the automated setup script to create all groups and permissions:

```bash
cd LibraryProject
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings'); import django; django.setup(); exec(open('setup_groups_permissions.py').read())"
```

Or use Django shell:

```bash
python manage.py shell
>>> exec(open('setup_groups_permissions.py').read())
```

The script will create:
- Viewers group with can_view_book permission
- Editors group with can_view_book, can_create_book, can_edit_book, can_manage_authors
- Admins group with all permissions

### Verify Setup

```bash
python manage.py shell
```

Then in the shell:

```python
from django.contrib.auth.models import Group, Permission
from relationship_app.models import Book

# List all groups
groups = Group.objects.all()
for group in groups:
    print(f"\nGroup: {group.name}")
    print(f"Permissions: {group.permissions.count()}")
    for perm in group.permissions.all():
        print(f"  - {perm.codename}")
```

Expected output:
```
Group: Viewers
Permissions: 1
  - can_view_book

Group: Editors
Permissions: 4
  - can_view_book
  - can_create_book
  - can_edit_book
  - can_manage_authors

Group: Admins
Permissions: 6
  - can_view_book
  - can_create_book
  - can_edit_book
  - can_delete_book
  - can_publish_book
  - can_manage_authors
```

## Managing Users and Groups

### Assigning a User to a Group

```python
from django.contrib.auth.models import User, Group

# Get user and group
user = User.objects.get(username='john_doe')
group = Group.objects.get(name='Editors')

# Assign user to group
user.groups.add(group)
print(f"User {user.username} added to {group.name} group")
```

### Removing a User from a Group

```python
from django.contrib.auth.models import User, Group

# Get user and group
user = User.objects.get(username='john_doe')
group = Group.objects.get(name='Viewers')

# Remove user from group
user.groups.remove(group)
print(f"User {user.username} removed from {group.name} group")
```

### Viewing User's Permissions

```python
from django.contrib.auth.models import User, Permission

user = User.objects.get(username='john_doe')

# Get all permissions through groups
group_permissions = Permission.objects.filter(group__user=user).distinct()

# Get direct permissions
direct_permissions = user.user_permissions.all()

# All permissions
all_permissions = (group_permissions | direct_permissions).distinct()

print(f"\nPermissions for user {user.username}:")
for perm in all_permissions:
    print(f"  - {perm.codename}: {perm.name}")
```

### Using the Helper Functions

The `setup_groups_permissions.py` script provides helper functions:

```python
# In Django shell
from setup_groups_permissions import *

# Assign user to group
assign_user_to_group('john_doe', 'Editors')

# Remove user from group
remove_user_from_group('john_doe', 'Viewers')

# List user's permissions
list_user_permissions('john_doe')

# List all groups
list_all_groups()
```

## Testing Permissions

### Test Scenario 1: Viewer Role (Read-Only Access)

1. Create a test user:
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User, Group

# Create test user
viewer = User.objects.create_user(username='test_viewer', password='testpass123')
viewer_group = Group.objects.get(name='Viewers')
viewer.groups.add(viewer_group)
print(f"Created test_viewer and assigned to Viewers group")
```

2. Login as test_viewer and visit:
   - `/relationship_app/books/` - Should be able to view books (200 OK)
   - `/relationship_app/books/add/` - Should get permission denied (403 Forbidden)
   - `/relationship_app/books/1/edit/` - Should get permission denied (403 Forbidden)
   - `/relationship_app/books/1/delete/` - Should get permission denied (403 Forbidden)

### Test Scenario 2: Editor Role (Create/Edit Access)

1. Create a test user:
```python
from django.contrib.auth.models import User, Group

# Create test user
editor = User.objects.create_user(username='test_editor', password='testpass123')
editor_group = Group.objects.get(name='Editors')
editor.groups.add(editor_group)
print(f"Created test_editor and assigned to Editors group")
```

2. Login as test_editor and verify:
   - `/relationship_app/books/` - Can view books (200 OK)
   - `/relationship_app/books/add/` - Can create books (200 OK)
   - `/relationship_app/books/1/edit/` - Can edit books (200 OK)
   - `/relationship_app/books/1/delete/` - Should get permission denied (403 Forbidden)

### Test Scenario 3: Admin Role (Full Access)

1. Create a test user:
```python
from django.contrib.auth.models import User, Group

# Create test user
admin_user = User.objects.create_user(username='test_admin', password='testpass123')
admin_group = Group.objects.get(name='Admins')
admin_user.groups.add(admin_group)
print(f"Created test_admin and assigned to Admins group")
```

2. Login as test_admin and verify:
   - `/relationship_app/books/` - Can view books (200 OK)
   - `/relationship_app/books/add/` - Can create books (200 OK)
   - `/relationship_app/books/1/edit/` - Can edit books (200 OK)
   - `/relationship_app/books/1/delete/` - Can delete books (200 OK)

### Test Scenario 4: No Permissions (Unauthenticated)

1. Access without logging in:
   - `/relationship_app/books/` - Redirects to login page
   - `/relationship_app/books/add/` - Redirects to login page

## Admin Panel Management

### Accessing Django Admin

1. Navigate to: `http://localhost:8000/admin/`
2. Login with superuser credentials (e.g., admin/admin123)

### Managing Groups in Admin Panel

1. Click on "Groups" in the left sidebar
2. View existing groups (Viewers, Editors, Admins)
3. Edit a group to add/remove permissions
4. Add new groups as needed

### Assigning Users to Groups in Admin

1. Click on "Users" in the left sidebar
2. Select a user to edit
3. Scroll down to "Groups" section
4. Select groups to add user to
5. Click "Save"

### Creating Custom Groups

1. Click on "Groups" in the left sidebar
2. Click "Add Group" button
3. Enter group name
4. Select permissions from the available list
5. Click "Save"

Example: Create a "Publishers" group:
- Name: Publishers
- Permissions: can_view_book, can_create_book, can_publish_book

## View-Level Permission Enforcement

The following views enforce permissions through the `@permission_required` decorator:

### list_books() View
- Required Permission: `can_view_book`
- Access: Users without permission see a warning message
- Behavior: Redirects to login if not authenticated

### add_book() View
- Required Permission: `can_create_book`
- Access: Returns 403 Forbidden if user lacks permission
- Behavior: Shows success message on book creation

### edit_book() View
- Required Permission: `can_edit_book`
- Access: Returns 403 Forbidden if user lacks permission
- Behavior: Shows success message on book update

### delete_book() View
- Required Permission: `can_delete_book`
- Access: Returns 403 Forbidden if user lacks permission
- Behavior: Shows success message on book deletion

## Troubleshooting

### Issue: "Permission does not exist" Error

**Solution**: Ensure migrations have been run:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Groups Not Showing Up

**Solution**: Run the setup script:
```bash
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings'); import django; django.setup(); exec(open('setup_groups_permissions.py').read())"
```

### Issue: User Can't Access Views After Assigning to Group

**Solution**: User may need to log out and log back in for permissions to refresh:
```python
# In Django shell
from django.contrib.auth.models import User
user = User.objects.get(username='username')
# Clear session
user.session_set.all().delete()
```

### Issue: Adding New Permissions

1. Add permission to Book model Meta class:
```python
permissions = [
    ("new_permission", "Display Name"),
]
```

2. Create migration:
```bash
python manage.py makemigrations
```

3. Apply migration:
```bash
python manage.py migrate
```

4. Assign to groups in Django admin or via shell

## Best Practices

1. **Always use groups for permission management** - Assign permissions to groups, not individual users
2. **Follow the principle of least privilege** - Give users minimum permissions needed
3. **Document custom groups** - Document any custom groups you create
4. **Audit permissions regularly** - Review group permissions and user assignments
5. **Use meaningful permission names** - Use clear codenames that describe the action
6. **Test permission changes** - Always test changes before deploying to production
7. **Log permission-sensitive actions** - Log access to sensitive operations

## Additional Resources

- [Django Permissions Documentation](https://docs.djangoproject.com/en/stable/topics/auth/default/#permissions-and-authorization)
- [Django Groups Documentation](https://docs.djangoproject.com/en/stable/topics/auth/default/#groups)
- [Django @permission_required Decorator](https://docs.djangoproject.com/en/stable/topics/auth/default/#the-permission-required-decorator)
