from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import EmployerViewSet, JobPostingViewSet, JobApplicationViewSet, EmployerFeedbackViewSet, RehireRequestViewSet

router = DefaultRouter()
router.register(r'employers', EmployerViewSet, basename='employer')
router.register(r'job-postings', JobPostingViewSet, basename='jobposting')
router.register(r'job-applications', JobApplicationViewSet, basename='jobapplication')
router.register(r'feedback', EmployerFeedbackViewSet, basename='employerfeedback')
router.register(r'rehire-requests', RehireRequestViewSet, basename='rehirerequest')

urlpatterns = [
    path('', include(router.urls)),
]
