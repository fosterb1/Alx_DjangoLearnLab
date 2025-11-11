from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Book

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'date_of_birth')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'