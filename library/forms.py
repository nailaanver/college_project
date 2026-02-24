from django import forms
from django.contrib.auth import get_user_model

from .models import Issue
from library.models import Book

from django.utils.timezone import now

# ✅ Always use the swapped user model
User = get_user_model()


# ==========================
# ISSUE BOOK FORM
# ==========================
class IssueBookForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['user', 'book', 'due_date']
        widgets = {
            'due_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only books with available copies
        self.fields['book'].queryset = Book.objects.filter(available_copies__gt=0)

        # All users (students)
        self.fields['user'].queryset = User.objects.all()

        # Optional styling
        self.fields['user'].widget.attrs.update({'class': 'form-control'})
        self.fields['book'].widget.attrs.update({'class': 'form-control'})
        
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        today = now().date()

        if due_date and due_date < today:
            raise forms.ValidationError("Due date cannot be in the past.")

        return due_date


# ==========================
# RETURN BOOK FORM
# ==========================
class ReturnBookForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['return_date']
        widgets = {
            'return_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            )
        }


# ==========================
# BOOK FORM
# ==========================
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
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'total_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_copies': forms.NumberInput(attrs={'class': 'form-control'}),
        }
