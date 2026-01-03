from django import forms
from django.contrib.auth import get_user_model
from .models import Teacher

User = get_user_model()

# Form to edit User fields
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# Form to edit Teacher fields
class TeacherForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Teacher
        fields = ['date_of_birth', 'subject', 'profile_photo']
