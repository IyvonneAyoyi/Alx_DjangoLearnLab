from django import forms
from .models import Post, Comment  # <-- import Comment model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]

# ----------------------------
# Comment Form
# ----------------------------
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        max_length=1000,
        label=''
    )

    class Meta:
        model = Comment
        fields = ['content']
