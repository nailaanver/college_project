from django import forms
from .models import Student
from django.core.exceptions import ValidationError
from datetime import date

class StudentForm(forms.ModelForm):
    # Add calendar picker and future date validation
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'}
        )
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
            'profile_photo',
        ]

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        if dob > date.today():
            raise ValidationError("Date of birth cannot be in the future")
        return dob
