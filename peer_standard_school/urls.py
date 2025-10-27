"""
URL configuration for peer_standard_school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_views import api_root
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('programs/', TemplateView.as_view(template_name='programs.html'), name='programs'),
    path('admissions/', TemplateView.as_view(template_name='admissions.html'), name='admissions'),
    path('recruitment/', TemplateView.as_view(template_name='recruitment.html'), name='recruitment'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('students/', include('students.urls')),
    path('courses/', include('courses.urls')),
    path('employers/', include('employers.urls')),
    path('certifications/', include('certifications.urls')),
    path('financials/', include('financials.urls')),

    # API URLs
    path('api/', api_root, name='api_root'),
    path('api/docs/', TemplateView.as_view(template_name='api_docs.html'), name='api_docs'),
    path('api/accounts/', include('accounts.api_urls')),
    path('api/courses/', include('courses.api_urls')),
    path('api/students/', include('students.api_urls')),
    path('api/employers/', include('employers.api_urls')),
    path('api/certifications/', include('certifications.api_urls')),
    path('api/financials/', include('financials.api_urls')),

    # JWT Token URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
