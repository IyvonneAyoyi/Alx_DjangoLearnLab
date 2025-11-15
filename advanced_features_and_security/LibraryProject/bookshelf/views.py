from django.shortcuts import render
from .forms import ExampleForm

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
