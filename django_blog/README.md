# Django Blog Project

This repository contains the initial setup and development of a Django-based blog application. The project includes a fully configured Django environment, the foundational blog model, static and template setup, and a complete user authentication system (registration, login, logout, and profile management).

---

## Project Setup and Configuration

### Environment & Framework Setup

* Django installed using `pip install django`.

* A new Django project created using:

  ```bash
  django-admin startproject django_blog
  ```

* Inside the project directory, a new application named **blog** was created:

  ```bash
  python manage.py startapp blog
  ```

* The `blog` app was added to `INSTALLED_APPS` in `django_blog/settings.py`.

---

## Database Configuration

The project currently uses Django's default **SQLite** database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

This setup is sufficient for development and initial testing.
Django automatically manages migrations and schema updates.

---

## Blog Model

A Blog **Post** model was created to represent articles authored by users.

### `Post` Model Structure

```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
```

### Database Migration Steps

```bash
python manage.py makemigrations blog
python manage.py migrate
```

The model now exists in the database and can be viewed/managed in Django Admin.

---

## Templates and Static File Setup

The required folder structure is added inside the **blog** app:

```
blog/
 ├── static/
 │     └── blog/
 │           ├── styles.css
 │           └── scripts.js
 └── templates/
       └── blog/
             ├── base.html
             ├── home.html
             ├── register.html
             ├── login.html
             ├── logout.html
             └── profile.html
```

Django was configured to detect these directories through the existing `TEMPLATES` and `STATIC_URL` settings.

---

## User Authentication System

The project includes a complete authentication system that allows users to:

### Register

Custom registration built using `UserCreationForm` (extended to include email).

### Log In / Log Out

Implemented using Django’s built-in authentication views.

### Manage Profile

Authenticated users can view and update their profile information (e.g., email).

### Form Validation & Security

* CSRF protection on all forms
* Secure password hashing handled by Django
* Login restricted to authenticated users

---

## Authentication Templates

The following templates were created and connected to the authentication views:

* `register.html`
* `login.html`
* `logout.html`
* `profile.html`

These templates include form rendering, validation messages, and UI structure.

---

## URL Configuration

Authentication URL patterns are defined in `blog/urls.py`:

```python
path('register/', views.register, name='register'),
path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
path('profile/', views.profile, name='profile'),
```

Included in the project's main `django_blog/urls.py`.

---

## Profile Management

A dedicated view allows logged-in users to:

* Access a personal profile page
* Update their information (e.g., email)
* Maintain secure and clean account data

This uses Django authentication decorators to ensure only logged-in users can access it.

---

## Testing the System

All parts of the authentication system have been tested manually:

### Registration

* New accounts can be created.
* Validation errors appear correctly.

### Login

* Only valid credentials allow access.
* Upon login, users are redirected correctly.

### Logout

* Session is cleared.
* Logout confirmation page displays.

### Profile

* Accessible only by authenticated users.
* User information updates successfully.

---

## Running the Project

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

The development server should load successfully, confirming templates, static files, and authentication flow.

---