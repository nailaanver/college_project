from django import forms
from .models import Teacher

class TeacherForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Teacher
        fields = [
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'subject',
            'profile_photo'
        ]
