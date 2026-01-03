from django import forms
from .models import Student
from django.core.exceptions import ValidationError
from datetime import date

class StudentForm(forms.ModelForm):

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    parent_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Parent Email'})
    )

    class Meta:
        model = Student
        fields = [
            'first_name',
            'last_name',
            'father_name',
            'mother_name',
            'register_number',
            'date_of_birth',
            'course',
            'semester',        # ✅ ADD THIS
            'profile_photo',
            'parent_email',
        ]
