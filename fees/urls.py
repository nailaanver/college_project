from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_fee_structure, name='create_fee'),
    path('list/', views.fee_list, name='fee_list'),
    
    
]
