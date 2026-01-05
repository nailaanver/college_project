from django.contrib import admin
from .models import Book, Issue

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'total_copies',
        'available_copies'
    )
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('category',)

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'book',
        'user',
        'issue_date',
        'due_date',
        'status',
        'fine'
    )
    list_filter = ('status', 'issue_date')
