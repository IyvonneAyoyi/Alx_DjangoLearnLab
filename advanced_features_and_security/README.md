# LibraryProject - Advanced Features and Security

A comprehensive Django library management system demonstrating advanced features and security best practices.

## Table of Contents

1. [Overview](#overview)
2. [Security Features](#security-features)
3. [Permissions and Groups](#permissions-and-groups)
4. [Project Structure](#project-structure)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Testing](#testing)
8. [Documentation](#documentation)

## Overview

LibraryProject is a Django application that demonstrates:
- Advanced Django features and patterns
- Comprehensive security implementations
- Role-based access control (RBAC)
- Custom permission management
- Secure form handling
- Authentication and authorization

## Security Features

### CSRF (Cross-Site Request Forgery) Protection
- CSRF tokens on all forms
- Secure cookie configuration
- Protected POST, PUT, DELETE endpoints

### XSS (Cross-Site Scripting) Prevention
- Django template auto-escaping
- Content Security Policy (CSP) headers
- Input validation and sanitization

### SQL Injection Prevention
- Django ORM for all database queries
- Parameterized queries
- No raw SQL execution

### Session Security
- HttpOnly session cookies
- Secure session timeout
- HTTPS-ready configuration

### Password Security
- Strong password validation
- Password hashing with PBKDF2
- Password strength requirements

### Browser Security Headers
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Strict-Transport-Security

## Permissions and Groups

### Custom Permissions

The application defines 6 custom permissions on the Book model:

| Permission | Code | Purpose |
|---|---|---|
| Can view book | `can_view_book` | View and list books |
| Can create book | `can_create_book` | Create new books |
| Can edit book | `can_edit_book` | Edit existing books |
| Can delete book | `can_delete_book` | Delete books |
| Can publish book | `can_publish_book` | Publish books |
| Can manage authors | `can_manage_authors` | Manage author relationships |

### Default Groups

**Viewers** - Read-only access
- Permissions: can_view_book

**Editors** - Create and modify content
- Permissions: can_view_book, can_create_book, can_edit_book, can_manage_authors

**Admins** - Full administrative control
- Permissions: All 6 permissions

### Permission Decorators

All protected views use Django's `@permission_required` decorator:

```python
@permission_required('relationship_app.can_create_book', raise_exception=True)
def add_book(request):
    # Only users with can_create_book permission can access
    pass
```

Unauthorized access returns HTTP 403 Forbidden.

## Project Structure

```
LibraryProject/
├── LibraryProject/          # Main project settings
│   ├── settings.py          # Django configuration with security settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI application
├── relationship_app/        # Book management app
│   ├── models.py            # Book, Author, Library, Librarian models
│   ├── views.py             # Protected views with permission decorators
│   ├── forms.py             # Secure forms with validation
│   ├── urls.py              # App URL patterns
│   └── templates/           # HTML templates with CSRF tokens
├── bookshelf/              # User and configuration app
│   ├── models.py           # CustomUser and Book models
│   ├── views.py            # Form example views
│   ├── forms.py            # Example forms
│   └── templates/          # Form templates
├── accounts/               # Account management app
│   ├── models.py           # Account models
│   ├── views.py            # Account views
│   └── forms.py            # Account forms
├── manage.py               # Django management utility
├── db.sqlite3              # SQLite database
└── setup_groups_permissions.py  # Script to initialize groups
```

## Installation

### Prerequisites
- Python 3.8+
- Django 5.2.6
- pip

### Setup Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd LibraryProject
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install django pillow
```

4. **Apply migrations:**
```bash
python manage.py migrate
```

5. **Create superuser:**
```bash
python manage.py createsuperuser
```

6. **Setup groups and permissions:**
```bash
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings'); import django; django.setup(); exec(open('setup_groups_permissions.py').read())"
```

7. **Run development server:**
```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`

## Usage

### Creating Test Users

In Django shell (`python manage.py shell`):

```python
from bookshelf.models import CustomUser
from django.contrib.auth.models import Group

# Create a viewer user
viewer = CustomUser.objects.create_user(
    username='viewer',
    email='viewer@example.com',
    password='viewerpass123'
)
viewer.groups.add(Group.objects.get(name='Viewers'))

# Create an editor user
editor = CustomUser.objects.create_user(
    username='editor',
    email='editor@example.com',
    password='editorpass123'
)
editor.groups.add(Group.objects.get(name='Editors'))
```

### Accessing Protected Views

- **View books:** `/relationship_app/books/` (requires can_view_book)
- **Add book:** `/relationship_app/books/add/` (requires can_create_book)
- **Edit book:** `/relationship_app/books/<id>/edit/` (requires can_edit_book)
- **Delete book:** `/relationship_app/books/<id>/delete/` (requires can_delete_book)

### Admin Interface

Access Django admin at `http://localhost:8000/admin/`

Features:
- Manage users and groups
- Assign users to groups
- Modify group permissions
- Manage books and authors

## Testing

### Run Automated Tests

Permission system tests:
```bash
python permissions_test.py
```

Django unit tests:
```bash
python manage.py test
```

### Manual Testing

1. **Test Viewer Access:**
   - Login as viewer user
   - Can view books
   - Cannot create/edit/delete books (403 Forbidden)

2. **Test Editor Access:**
   - Login as editor user
   - Can view, create, and edit books
   - Cannot delete books (403 Forbidden)

3. **Test Admin Access:**
   - Login as admin user
   - Can perform all operations

## Documentation

### Comprehensive Guides

- **PERMISSIONS_GUIDE.md** - Complete permissions and groups documentation
- **PERMISSIONS_QUICK_REFERENCE.md** - Quick testing reference
- **SECURITY_DOCUMENTATION.md** - Security features documentation
- **IMPLEMENTATION_SUMMARY.md** - Implementation overview

### View Documentation

Each view in `relationship_app/views.py` includes security documentation explaining:
- Permission requirements
- CSRF protection
- Input validation
- Error handling

## Database Models

### Book Model (bookshelf)
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    publication_date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### CustomUser Model (bookshelf)
```python
class CustomUser(AbstractUser):
    date_of_birth = models.DateField()
    profile_photo = models.ImageField()
```

### UserProfile Model (relationship_app)
```python
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
```

## Security Configuration

### CSRF Settings
```python
CSRF_COOKIE_SECURE = False  # Set to True in production
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000']
```

### Session Settings
```python
SESSION_COOKIE_SECURE = False  # Set to True in production
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1800  # 30 minutes
```

### Security Headers
```python
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_SECURITY_POLICY = {...}
```

## Environment Configuration

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Set `ALLOWED_HOSTS` to your domain
3. Set `CSRF_COOKIE_SECURE = True`
4. Set `SESSION_COOKIE_SECURE = True`
5. Use HTTPS/SSL
6. Use PostgreSQL instead of SQLite
7. Set secure `SECRET_KEY`

## Troubleshooting

### Migrations Not Applied
```bash
python manage.py makemigrations
python manage.py migrate
```

### Permission Denied (403)
- Ensure user is in correct group
- Check group has required permission
- Verify permission decorator syntax

### Groups Don't Exist
```bash
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings'); import django; django.setup(); exec(open('setup_groups_permissions.py').read())"
```

## Contributing

Contributions are welcome! Please ensure:
- Code follows Django best practices
- Security best practices are maintained
- All tests pass
- Documentation is updated

## License

This project is part of the ALX Django Learning Lab curriculum.

## Support

For issues or questions:
1. Check the documentation files
2. Review the PERMISSIONS_QUICK_REFERENCE.md
3. Consult SECURITY_DOCUMENTATION.md

## Version History

### v1.0.0 (Current)
- Django 5.2.6 support
- CSRF, XSS, SQL injection protection
- Custom permissions and groups
- Role-based access control
- Comprehensive documentation
- Automated testing suite
