from django.urls import path
from . import views

app_name = 'employers'

urlpatterns = [
    path('', views.employer_list, name='list'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('post-job/', views.post_job, name='post_job'),
    path('jobs/', views.job_list, name='jobs'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/edit/', views.job_edit, name='job_edit'),
    path('<int:employer_id>/', views.employer_detail, name='detail'),
]
