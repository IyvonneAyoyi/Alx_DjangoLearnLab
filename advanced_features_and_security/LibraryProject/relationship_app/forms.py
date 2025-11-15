# relationship_app/forms.py
from django import forms
from .models import Book  

class BookForm(forms.ModelForm):
    """
    BookForm - Secure Form for Book Management
    
    Security Features:
    1. CSRF Protection: Django automatically includes CSRF token in form rendering
    2. Input Validation: All fields are validated using Django's form validation system
    3. XSS Prevention: All form data is automatically escaped when rendered in templates
    4. SQL Injection Prevention: ModelForm uses Django ORM which parameterizes all queries
    5. HTML5 Validation: Browser-level validation as a first defense (not relied upon)
    """
    
    class Meta:
        model = Book
        fields = '__all__'
        # Security: Explicitly specifying fields prevents mass assignment vulnerabilities
        # If a new field is added to the model, it won't be automatically editable in forms
        # This requires developers to explicitly enable new fields  
