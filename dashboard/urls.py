from django.urls import path
from . import views

urlpatterns = [
    # path('', views.splash, name='splash'),          # /home/  → splash
    path('', views.home, name='home'), 
    path('add-timetable/', views.add_timetable, name='add-timetable'),
    path('timetable/', views.timetable_filter, name='timetable-filter'),
    path('timetable/view/', views.timetable_view, name='timetable-view'),

]