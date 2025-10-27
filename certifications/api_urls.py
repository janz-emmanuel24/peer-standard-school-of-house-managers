from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CertificateTemplateViewSet, CertificateViewSet, CertificateVerificationViewSet, AccreditationViewSet, CourseAccreditationViewSet, CompetencyAssessmentViewSet

router = DefaultRouter()
router.register(r'templates', CertificateTemplateViewSet, basename='certificatetemplate')
router.register(r'certificates', CertificateViewSet, basename='certificate')
router.register(r'verifications', CertificateVerificationViewSet, basename='certificateverification')
router.register(r'accreditations', AccreditationViewSet, basename='accreditation')
router.register(r'course-accreditations', CourseAccreditationViewSet, basename='courseaccreditation')
router.register(r'competency-assessments', CompetencyAssessmentViewSet, basename='competencyassessment')

urlpatterns = [
    path('', include(router.urls)),
]
