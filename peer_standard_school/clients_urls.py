"""
URL configuration for clients pages.
"""
from django.urls import path
from django.views.generic import TemplateView

app_name = 'clients'

urlpatterns = [
    path('', TemplateView.as_view(template_name='clients/index.html'), name='index'),
    path('workers/', TemplateView.as_view(template_name='clients/workers.html'), name='workers'),
    path('house-owners/', TemplateView.as_view(template_name='clients/house_owners.html'), name='house_owners'),
    path('patients/', TemplateView.as_view(template_name='clients/patients.html'), name='patients'),
    path('organisations/', TemplateView.as_view(template_name='clients/organisations.html'), name='organisations'),
    path('companies/', TemplateView.as_view(template_name='clients/companies.html'), name='companies'),
    path('building-owners/', TemplateView.as_view(template_name='clients/building_owners.html'), name='building_owners'),
]

