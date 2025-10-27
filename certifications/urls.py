from django.urls import path
from . import views

app_name = 'certifications'

urlpatterns = [
    path('', views.certificate_list, name='list'),
    path('verify/', views.verify_certificate, name='verify'),
    path('templates/', views.template_list, name='templates'),
    path('templates/create/', views.template_create, name='template_create'),
    path('<int:certificate_id>/', views.certificate_detail, name='detail'),
    path('<int:certificate_id>/download/', views.certificate_download, name='download'),
]
