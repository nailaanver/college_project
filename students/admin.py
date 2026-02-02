from django.contrib import admin
from .models import Student,Semester



    
from django.contrib import admin
from .models import Student
from students.utils.semester import promote_students_of_semester




@admin.action(description="Promote ALL students of selected semester")
def promote_whole_semester(modeladmin, request, queryset):
    semesters = set(queryset.values_list('semester', flat=True))

    messages = []

    for sem in semesters:
        count, msg = promote_students_of_semester(sem)
        messages.append(f"Semester {sem}: {msg} ({count})")

    modeladmin.message_user(request, " | ".join(messages))
    
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('register_number', 'first_name', 'semester', 'course')
    list_filter = ('semester', 'course')
    actions = [promote_whole_semester]
