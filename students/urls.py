from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list, name='list'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('certificates/', views.my_certificates, name='certificates'),
    path('enrollments/', views.enrollment_list, name='enrollments'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll'),
    path('<int:student_id>/', views.student_detail, name='detail'),
    path('<int:student_id>/edit/', views.student_edit, name='edit'),
]
