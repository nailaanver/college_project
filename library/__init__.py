


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    from django.utils.timezone import now

    self.fields['book'].queryset = Book.objects.filter(available_copies__gt=0)
    self.fields['user'].queryset = User.objects.all()

    self.fields['user'].widget.attrs.update({'class': 'form-control'})
    self.fields['book'].widget.attrs.update({'class': 'form-control'})

    # ✅ Prevent past date selection in UI
    self.fields['due_date'].widget.attrs['min'] = now().date().isoformat()