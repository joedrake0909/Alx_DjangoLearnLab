from django import models
from django import forms
from .models import Book

class ExampleForm(forms.Form):
    # A simple search form to demonstrate secure input handling
    search_query = forms.CharField(max_length=100, required=False, label='Search Books')

class BookForm(forms.ModelForm):
    # A form for creating or editing books securely
    class Meta:
        model = Book
        fields = ['title', 'author', 'library']