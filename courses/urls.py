from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='list'),
    path('create/', views.course_create, name='create'),
    path('<int:course_id>/', views.course_detail, name='detail'),
    path('<int:course_id>/edit/', views.course_edit, name='edit'),
    path('<int:course_id>/enroll/', views.course_enroll, name='enroll'),
    path('categories/', views.category_list, name='categories'),
]
