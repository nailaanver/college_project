from django.urls import path
from .views import upload_face

urlpatterns = [
    path('upload-face/', upload_face, name='upload-face'),
]
