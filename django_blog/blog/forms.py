# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from taggit.forms import TagWidget
from .models import Post, Comment, Tag

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts
    
    Fields:
        - title: CharField with minimum 5 characters validation
        - content: TextField for post body
        - tags: ManyToMany field for categorization (custom Tag model)
        - taggit_tags: django-taggit integration for tag management with TagWidget
    
    Features:
        - Custom validation for title length
        - Bootstrap-styled form controls
        - Placeholder text for user guidance
        - Tag input with comma-separated values using TagWidget()
        - Supports both custom Tag model and django-taggit
        - Author field excluded (set automatically in view)
    """
    tags_input = forms.CharField(
        required=False,
        widget=TagWidget(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., Django, Python, Web)',
            'data-role': 'tagsinput'
        }),
        help_text='Separate tags with commas - uses django-taggit TagWidget'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Pre-populate tags for editing (using both custom tags and taggit)
            custom_tags = ', '.join([tag.name for tag in self.instance.tags.all()])
            taggit_tags = ', '.join([tag.name for tag in self.instance.taggit_tags.all()])
            # Combine both tag sources
            all_tags = set(filter(None, custom_tags.split(', ') + taggit_tags.split(', ')))
            self.initial['tags_input'] = ', '.join(sorted(all_tags))
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError("Title must be at least 5 characters long.")
        return title
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        
        # Handle tags with both custom Tag model and django-taggit
        if 'tags_input' in self.cleaned_data:
            tags_input = self.cleaned_data['tags_input']
            
            # Clear existing tags
            instance.tags.clear()
            instance.taggit_tags.clear()
            
            if tags_input:
                tag_names = [name.strip() for name in tags_input.split(',') if name.strip()]
                for tag_name in tag_names:
                    # Add to custom Tag model
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    instance.tags.add(tag)
                
                # Add to django-taggit (preferred method)
                instance.taggit_tags.add(*tag_names)
        
        return instance

class CommentForm(forms.ModelForm):
    """
    Form for creating and editing comments
    
    Fields:
        - content: TextField for comment text
    
    Features:
        - Bootstrap-styled textarea
        - Placeholder text
        - Validation for non-empty content
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4
            }),
        }
        labels = {
            'content': 'Comment'
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 3:
            raise ValidationError("Comment must be at least 3 characters long.")
        return content