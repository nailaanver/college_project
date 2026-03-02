"""
URL configuration for college_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

# from dashboard.views import splash


urlpatterns = [
        path('', RedirectView.as_view(url='/home/', permanent=False)),  # 👈 FIX

    path('admin/', admin.site.urls),
    path('home/', include('dashboard.urls')),  # home page
    path('', include('accounts.urls')),
    path('adminpanel/', include('adminpanel.urls')),
    path('student/', include('students.urls')),
    path('teacher/', include('teachers.urls')),
    path('parent/', include('parents.urls')),
    path('attendance/',include('attendance.urls')),
    path('library/', include('library.urls')),
    
    path('internal-marks/', include('internal_marks.urls')),
    path('api/fees/', include('fees.api_urls')),
    path('fees/', include('fees.urls')),
    path('ai/', include('ai_services.urls')),
    path('notifications/', include('notifications.urls')),
    

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path("favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "favicon.ico")),
]