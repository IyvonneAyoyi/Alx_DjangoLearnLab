from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .forms import ExampleForm
from .models import Book

# Create your views here.

def form_example(request):
    """
    View for demonstrating secure form handling with Django.
    
    Security features demonstrated:
    - CSRF token validation
    - Form input validation
    - XSS prevention via auto-escaping
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process form data safely
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            
            # Data is sanitized and safe to use
            return render(request, 'bookshelf/form_example.html', {
                'form': ExampleForm(),
                'success': True
            })
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})


@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    """
    List all books with can_view_book permission check.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create_book', raise_exception=True)
def create_book(request):
    """
    Create a new book with can_create_book permission check.
    """
    if request.method == 'POST':
        # Handle book creation
        title = request.POST.get('title')
        author = request.POST.get('author')
        
        if title and author:
            book = Book.objects.create(
                title=title,
                author=author
            )
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('bookshelf:book_list')
    
    return render(request, 'bookshelf/create_book.html')


@permission_required('bookshelf.can_edit_book', raise_exception=True)
def edit_book(request, book_id):
    """
    Edit an existing book with can_edit_book permission check.
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.save()
        messages.success(request, f'Book "{book.title}" updated successfully!')
        return redirect('bookshelf:book_list')
    
    return render(request, 'bookshelf/edit_book.html', {'book': book})


@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """
    Delete a book with can_delete_book permission check.
    """
    book = get_object_or_404(Book, id=book_id)
    book_title = book.title
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('bookshelf:book_list')
    
    return render(request, 'bookshelf/delete_book.html', {'book': book})
