from django.urls import path
from . import views

urlpatterns = [
    path('issue/', views.issue_book, name='issue-book'),
    path('return/', views.return_book_list, name='return-book-list'),
    path('return/<int:issue_id>/', views.return_book, name='return-book'),
    path('my-library/', views.my_library, name='my-library'),
    path('reports/', views.library_reports, name='library-reports'),
    
    path('books/', views.book_list, name='book-list'),
    path('books/add/', views.book_add, name='book-add'),
    path('books/edit/<int:book_id>/', views.book_edit, name='book-edit'),
    path('books/delete/<int:book_id>/', views.book_delete, name='book-delete'),

]
