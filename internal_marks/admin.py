from django.contrib import admin
from .models import InternalMark

@admin.register(InternalMark)
class InternalMarkAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'subject',
        'test1',
        'test2',
        'assignment',
        'attendance_mark',
        'total_internal',
        'status',
    )
    list_filter = ('subject', 'status')
    search_fields = ('student__register_number',)
