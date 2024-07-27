from django import forms
from .models import Book, Author, Genre
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('regular', 'Regular User'),
        ('librarian', 'Librarian'),
        ('admin', 'Admin'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, help_text="Select the user's role.")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        
        if role == 'librarian':
            librarians_group, created = Group.objects.get_or_create(name='Librarians')
            if commit:
                user.save()
                user.groups.add(librarians_group)
        elif role == 'admin':
            user.is_superuser = True
            user.is_staff = True
            if commit:
                user.save()
        else:
            if commit:
                user.save()

        return user

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'isbn', 'genre', 'status']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'biography', 'nationality']

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']