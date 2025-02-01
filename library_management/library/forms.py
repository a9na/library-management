from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'isbn', 'image', 'available', 'is_recommended']



class CustomUserCreationForm(UserCreationForm):
    # Define the choices for user_type
    USER_TYPE_CHOICES = [
        ('reader', 'Reader'),
        ('librarian', 'Librarian'),
    ]
    
    # Add a user_type field to the form
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.Select)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']  # Include all fields you want in the form

