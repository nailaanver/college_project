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
    
    path('my-library/', views.my_library, name='my-library'),
    path('library/search/', views.user_book_search, name='user-book-search'),
    path('menu/', views.library_menu, name='library-menu'),
    
    # path('pay-fine/<int:issue_id>/', views.pay_library_fine, name='pay_library_fine'),
    path(
    "teacher-pay-fine/<int:issue_id>/",
    views.teacher_pay_fine,
    name="teacher_pay_fine"
),
    path('student/', views.student_library, name='student-library'),
    path('teacher/', views.teacher_library, name='teacher-library'),
    
    path('pay-fine/<int:issue_id>/', views.pay_fine, name='pay-fine'),
    path('execute-teacher-fine/<int:issue_id>/', views.execute_teacher_fine, name='execute-teacher-fine'),
    path('payment-success/', views.payment_success, name='payment-success'),
    path('payment-cancel/', views.payment_cancel, name='payment-cancel'),
]
