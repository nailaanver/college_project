from django import forms
from .models import FeeStructure
from students.models import Student

class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['fee_type', 'course', 'semester', 'amount']
        widgets = {
            'semester': forms.NumberInput(attrs={'min': 1}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }
