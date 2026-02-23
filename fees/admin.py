from django.contrib import admin
from .models import Fee
from .models import TeacherLibraryFine

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_type', 'amount', 'due_date', 'is_paid')
    list_filter = ('fee_type', 'is_paid')
    search_fields = ('student__register_number',)
    
admin.site.register(TeacherLibraryFine)
