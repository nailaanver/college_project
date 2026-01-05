from django import forms
from .models import Issue
from django.contrib.auth.models import User
from library.models import Book

class IssueBookForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['user', 'book', 'due_date']

    # Optional: filter only available books
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(available_copies__gt=0)
        self.fields['user'].queryset = User.objects.all()
        self.fields['due_date'].widget.attrs.update({'type': 'date'})

from django import forms
from .models import Issue

class ReturnBookForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['return_date']  # only need return date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['return_date'].widget.attrs.update({'type': 'date'})
        
        
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'isbn',
            'category',
            'total_copies',
            'available_copies',
        ]

