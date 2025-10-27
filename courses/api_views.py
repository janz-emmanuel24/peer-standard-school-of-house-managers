from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from .models import CourseCategory, Course, CourseModule, Instructor, CourseInstructor, Assessment
from .serializers import (
    CourseCategorySerializer, CourseSerializer, CourseListSerializer,
    CourseModuleSerializer, InstructorSerializer, CourseInstructorSerializer,
    AssessmentSerializer
)


class CourseCategoryViewSet(viewsets.ModelViewSet):
    """Course category viewset"""
    queryset = CourseCategory.objects.filter(is_active=True)
    serializer_class = CourseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin and instructors can modify categories
            if not (self.request.user.is_authenticated and self.request.user.user_type in ['admin', 'instructor']):
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class CourseViewSet(viewsets.ModelViewSet):
    """Course viewset"""
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseSerializer
    
    def get_queryset(self):
        queryset = Course.objects.all()
        status_filter = self.request.query_params.get('status', None)
        category = self.request.query_params.get('category', None)
        difficulty = self.request.query_params.get('difficulty', None)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if category:
            queryset = queryset.filter(category_id=category)
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
        
        return queryset.select_related('category', 'created_by').prefetch_related('modules', 'assessments')
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin and instructors can modify courses
            if not self.request.user.user_type in ['admin', 'instructor']:
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """Get course enrollments"""
        course = self.get_object()
        enrollments = course.enrollments.select_related('student__user').all()
        
        from students.serializers import EnrollmentSerializer
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get course statistics"""
        course = self.get_object()
        
        stats = {
            'total_enrollments': course.enrollments.count(),
            'active_enrollments': course.enrollments.filter(status='enrolled').count(),
            'completed_enrollments': course.enrollments.filter(status='completed').count(),
            'completion_rate': 0,
            'average_score': 0,
            'instructor_count': course.courseinstructor_set.count(),
            'module_count': course.modules.count(),
            'assessment_count': course.assessments.count(),
        }
        
        if stats['total_enrollments'] > 0:
            stats['completion_rate'] = (stats['completed_enrollments'] / stats['total_enrollments']) * 100
        
        # Calculate average score from assessment results
        from students.models import AssessmentResult
        avg_score = AssessmentResult.objects.filter(
            enrollment__course=course
        ).aggregate(avg=Avg('score'))['avg']
        
        if avg_score:
            stats['average_score'] = round(avg_score, 2)
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular courses"""
        courses = Course.objects.annotate(
            enrollment_count=Count('enrollments')
        ).order_by('-enrollment_count')[:10]
        
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search courses"""
        query = request.query_params.get('q', '')
        queryset = self.get_queryset()
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(learning_outcomes__icontains=query)
            )
        
        serializer = CourseListSerializer(queryset, many=True)
        return Response(serializer.data)


class CourseModuleViewSet(viewsets.ModelViewSet):
    """Course module viewset"""
    queryset = CourseModule.objects.all()
    serializer_class = CourseModuleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_id = self.request.query_params.get('course', None)
        if course_id:
            return CourseModule.objects.filter(course_id=course_id).order_by('order')
        return CourseModule.objects.all()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin and instructors can modify modules
            if not self.request.user.user_type in ['admin', 'instructor']:
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class InstructorViewSet(viewsets.ModelViewSet):
    """Instructor viewset"""
    queryset = Instructor.objects.filter(is_active=True)
    serializer_class = InstructorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify instructors
            if not self.request.user.user_type == 'admin':
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        """Get instructor's courses"""
        instructor = self.get_object()
        courses = Course.objects.filter(
            courseinstructor__instructor=instructor
        ).select_related('category')
        
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)


class AssessmentViewSet(viewsets.ModelViewSet):
    """Assessment viewset"""
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_id = self.request.query_params.get('course', None)
        if course_id:
            return Assessment.objects.filter(course_id=course_id)
        return Assessment.objects.all()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin and instructors can modify assessments
            if not self.request.user.user_type in ['admin', 'instructor']:
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
