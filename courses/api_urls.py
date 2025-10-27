from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CourseCategoryViewSet, CourseViewSet, CourseModuleViewSet, InstructorViewSet, AssessmentViewSet

router = DefaultRouter()
router.register(r'categories', CourseCategoryViewSet, basename='coursecategory')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'modules', CourseModuleViewSet, basename='coursemodule')
router.register(r'instructors', InstructorViewSet, basename='instructor')
router.register(r'assessments', AssessmentViewSet, basename='assessment')

urlpatterns = [
    path('', include(router.urls)),
]
