from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student
from fees.utils import generate_fees_for_student

@receiver(post_save, sender=Student)
def create_student_fees(sender, instance, created, **kwargs):
    if created:
        generate_fees_for_student(instance)
