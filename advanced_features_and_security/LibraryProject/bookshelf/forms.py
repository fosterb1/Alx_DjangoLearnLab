# bookshelf/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import escape
import re
from .models import Book, CustomUser

class ExampleForm(forms.Form):
    """
    ExampleForm demonstrates secure form handling practices.
    Includes validation, sanitization, and security measures.
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
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message',
            'rows': 4
        }),
        required=True
    )
    
    age = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=150,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age'
        })
    )
    
    agree_to_terms = forms.BooleanField(
        required=True,
        label="I agree to the terms and conditions"
    )

    def clean_name(self):
        """Custom validation for name field to prevent XSS and injection"""
        name = self.cleaned_data['name']
        
        # Remove any potential HTML/script tags
        cleaned_name = escape(name)
        
        # Check for suspicious patterns
        if re.search(r'[<>{}]', name):
            raise ValidationError("Name contains invalid characters.")
            
        # Limit length for security
        if len(name) > 100:
            raise ValidationError("Name is too long.")
            
        return cleaned_name

    def clean_message(self):
        """Secure message validation"""
        message = self.cleaned_data['message']
        
        # Sanitize message while preserving line breaks
        cleaned_message = escape(message)
        
        # Check for excessive length
        if len(message) > 1000:
            raise ValidationError("Message is too long. Maximum 1000 characters allowed.")
            
        return cleaned_message

    def clean(self):
        """Form-wide validation and security checks"""
        cleaned_data = super().clean()
        
        # Additional security checks can be added here
        email = cleaned_data.get('email')
        name = cleaned_data.get('name')
        
        # Example: Check for suspicious email patterns
        if email and re.search(r'(alert|script|javascript|onload|onerror)=', email.lower()):
            raise ValidationError("Invalid email format.")
            
        return cleaned_data

class BookForm(forms.ModelForm):
    """
    Secure ModelForm for Book model with additional validation.
    Demonstrates proper security practices for model forms.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'published_date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter author name'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ISBN number'
            }),
            'published_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book description',
                'rows': 4
            }),
        }

    def clean_title(self):
        """Secure title validation"""
        title = self.cleaned_data['title']
        
        # Sanitize title
        cleaned_title = escape(title.strip())
        
        # Validate length
        if len(cleaned_title) < 2:
            raise ValidationError("Title is too short.")
        if len(cleaned_title) > 200:
            raise ValidationError("Title is too long.")
            
        return cleaned_title

    def clean_isbn(self):
        """ISBN validation with security considerations"""
        isbn = self.cleaned_data['isbn']
        
        # Remove any non-alphanumeric characters for security
        clean_isbn = re.sub(r'[^a-zA-Z0-9]', '', isbn)
        
        # Basic ISBN validation (10 or 13 digits)
        if not re.match(r'^(\d{10}|\d{13})$', clean_isbn):
            raise ValidationError("Please enter a valid ISBN (10 or 13 digits).")
            
        return clean_isbn

    def clean_description(self):
        """Secure description validation"""
        description = self.cleaned_data.get('description', '')
        
        if description:
            # Sanitize while preserving some formatting
            cleaned_description = escape(description)
            
            # Limit length for security and performance
            if len(cleaned_description) > 2000:
                raise ValidationError("Description is too long. Maximum 2000 characters allowed.")
                
        return description

class SecureSearchForm(forms.Form):
    """
    Secure search form demonstrating safe input handling.
    Prevents SQL injection and XSS attacks.
    """
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books...',
            'aria-label': 'Search books'
        })
    )
    
    search_type = forms.ChoiceField(
        choices=[
            ('title', 'Title'),
            ('author', 'Author'),
            ('isbn', 'ISBN')
        ],
        initial='title',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    def clean_query(self):
        """Secure query sanitization"""
        query = self.cleaned_data['query']
        
        if query:
            # Sanitize search query
            clean_query = escape(query.strip())
            
            # Check for suspicious patterns
            suspicious_patterns = [
                r'(\b(OR|AND|SELECT|INSERT|UPDATE|DELETE|DROP|UNION)\b)',
                r'(\-\-|\/\*|\*\/)',
                r'(\b(script|javascript|onload|onerror)\b)'
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, clean_query, re.IGNORECASE):
                    raise ValidationError("Invalid search query.")
                    
            # Limit length
            if len(clean_query) > 100:
                raise ValidationError("Search query is too long.")
                
        return clean_query

class UserRegistrationForm(forms.ModelForm):
    """
    Secure user registration form with password validation.
    Demonstrates security best practices for user creation.
    """
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        min_length=8,
        label="Password"
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        }),
        label="Confirm Password"
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'date_of_birth']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

    def clean_email(self):
        """Email validation and sanitization"""
        email = self.cleaned_data['email']
        return escape(email.lower().strip())

    def clean_first_name(self):
        """Secure first name validation"""
        first_name = self.cleaned_data['first_name']
        return escape(first_name.strip())

    def clean_last_name(self):
        """Secure last name validation"""
        last_name = self.cleaned_data['last_name']
        return escape(last_name.strip())

    def clean(self):
        """Form-wide validation including password matching"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        # Additional security checks
        if password1:
            if len(password1) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
            if password1.isdigit():
                raise ValidationError("Password cannot be entirely numeric.")

        return cleaned_data

    def save(self, commit=True):
        """Secure user saving with password hashing"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user