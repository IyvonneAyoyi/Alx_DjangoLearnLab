from django.shortcuts import render, get_object_or_404
from .models import Book 
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import user_passes_test
from .forms import BookForm


# =====================================================
# SECURITY BEST PRACTICES IN VIEWS
# =====================================================

# Function-based view to list all books
def list_books(request):
    # Security: Using Django ORM (Book.objects.all()) prevents SQL injection
    # The ORM properly parameterizes queries and escapes data
    books = Book.objects.all()
    
    # Security: Django automatically escapes context data in templates
    # This prevents XSS attacks by converting special characters to HTML entities
    return render(request, 'relationship_app/list_books.html', {'books': books})



# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    # Security: Using Django's get_object_or_404() automatically validates the primary key
    # This prevents unauthorized access to resources and handles SQL injection prevention through ORM

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages


# User registration view
def register(request):
    # Security: UserCreationForm includes built-in password validation
    # - Prevents passwords that are too similar to username
    # - Enforces minimum length requirements
    # - Checks against common passwords dictionary
    # - Validates against purely numeric passwords
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Security: form.save() creates the user with hashed passwords via set_password()
            # Passwords are never stored in plain text
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# User login view
def login_view(request):
    # Security: AuthenticationForm protects against timing attacks on password checking
    # It uses constant-time comparison to check passwords regardless of where they fail
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Security: authenticate() uses password hashing (PBKDF2 by default) for comparison
            # It never compares plain text passwords
            user = authenticate(username=username, password=password)
            if user is not None:
                # Security: login() sets secure session cookies configured in settings.py
                login(request, user)
                return redirect('list_books')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})


# User logout view
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')



# Helper functions to check roles
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Role-based views
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm

# Add Book view
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    # Security: @permission_required decorator enforces authorization
    # It checks if the user has the 'can_add_book' permission before executing the view
    # raise_exception=True returns HTTP 403 Forbidden for unauthorized access
    if request.method == 'POST':
        form = BookForm(request.POST)
        # Security: ModelForm validation prevents invalid data and SQL injection
        # Form.is_valid() sanitizes and validates all input fields
        if form.is_valid():
            # Security: form.save() uses parameterized queries through Django ORM
            # This prevents SQL injection attacks
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})


# Edit Book view
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    # Security: @permission_required decorator enforces authorization
    # It checks if the user has the 'can_change_book' permission before executing the view
    # Security: get_object_or_404() validates the pk parameter and prevents information disclosure
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        # Security: ModelForm validation prevents invalid data and SQL injection
        if form.is_valid():
            # Security: form.save() uses parameterized queries - prevents SQL injection
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form})


# Delete Book view
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    # Security: @permission_required decorator enforces authorization
    # It checks if the user has the 'can_delete_book' permission before executing the view
    # Security: get_object_or_404() validates the pk parameter and prevents information disclosure
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # Security: Only POST requests with valid CSRF token can delete objects
        # CSRF token is checked by CsrfViewMiddleware (enabled by default)
        book.delete()
        return redirect('list_books')
    # Security: GET requests display confirmation page but don't perform deletion
    return render(request, 'relationship_app/delete_book.html', {'book': book})
