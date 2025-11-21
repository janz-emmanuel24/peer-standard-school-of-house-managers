"""
URL configuration for services pages.
"""
from django.urls import path
from django.views.generic import TemplateView

app_name = 'services'

urlpatterns = [
    path('', TemplateView.as_view(template_name='services/index.html'), name='index'),
    path('workers-training/', TemplateView.as_view(template_name='services/workers_training.html'), name='workers_training'),
    path('recruitment/', TemplateView.as_view(template_name='services/recruitment.html'), name='recruitment'),
    path('workers-management/', TemplateView.as_view(template_name='services/workers_management.html'), name='workers_management'),
    path('professional-cleaning/', TemplateView.as_view(template_name='services/professional_cleaning.html'), name='professional_cleaning'),
    path('elderly-care/', TemplateView.as_view(template_name='services/elderly_care.html'), name='elderly_care'),
]

