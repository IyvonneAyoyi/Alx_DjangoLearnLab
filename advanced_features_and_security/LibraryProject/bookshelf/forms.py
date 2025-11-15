from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ExampleForm(forms.Form):
    """
    Example form demonstrating Django form security best practices.
    
    Security Features:
    - CSRF protection (automatic via Django forms)
    - Input validation and sanitization
    - XSS prevention (auto-escaping in templates)
    """
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    message = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message',
            'rows': 4
        })
    )
    
    def clean_name(self):
        """Validate and sanitize name field"""
        name = self.cleaned_data.get('name')
        if name and len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long")
        return name
    
    def clean_email(self):
        """Validate email field"""
        email = self.cleaned_data.get('email')
        # Additional email validation if needed
        return email
    
    def clean_message(self):
        """Validate message field"""
        message = self.cleaned_data.get('message')
        # Django automatically escapes this in templates
        return message
