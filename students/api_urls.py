from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import StudentViewSet, EnrollmentViewSet, AttendanceViewSet, AssessmentResultViewSet, ProgressReportViewSet, PlacementViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'assessment-results', AssessmentResultViewSet, basename='assessmentresult')
router.register(r'progress-reports', ProgressReportViewSet, basename='progressreport')
router.register(r'placements', PlacementViewSet, basename='placement')

urlpatterns = [
    path('', include(router.urls)),
]
