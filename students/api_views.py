from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from .models import Student, Enrollment, Attendance, AssessmentResult, ProgressReport, Placement
from .serializers import (
    StudentSerializer, EnrollmentSerializer, AttendanceSerializer,
    AssessmentResultSerializer, ProgressReportSerializer, PlacementSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    """Student viewset"""
    queryset = Student.objects.filter(is_active=True)
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Student.objects.all()
        elif user.user_type == 'instructor':
            return Student.objects.filter(is_active=True)
        elif hasattr(user, 'student_profile'):
            return Student.objects.filter(id=user.student_profile.id)
        else:
            return Student.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify students
            if not (self.request.user.is_authenticated and self.request.user.user_type == 'admin'):
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """Get student enrollments"""
        student = self.get_object()
        enrollments = student.enrollments.select_related('course').all()
        
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def certificates(self, request, pk=None):
        """Get student certificates"""
        student = self.get_object()
        certificates = student.certificates.select_related('course').all()
        
        from certifications.serializers import CertificateSerializer
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Get student progress summary"""
        student = self.get_object()
        
        progress_data = {
            'total_enrollments': student.enrollments.count(),
            'completed_courses': student.enrollments.filter(status='completed').count(),
            'active_enrollments': student.enrollments.filter(status='enrolled').count(),
            'certificates_earned': student.certificates.count(),
            'average_score': 0,
            'attendance_rate': 0,
        }
        
        # Calculate average score
        avg_score = AssessmentResult.objects.filter(
            enrollment__student=student
        ).aggregate(avg=Avg('score'))['avg']
        
        if avg_score:
            progress_data['average_score'] = round(avg_score, 2)
        
        # Calculate attendance rate
        total_attendance = Attendance.objects.filter(
            enrollment__student=student
        ).count()
        
        if total_attendance > 0:
            present_count = Attendance.objects.filter(
                enrollment__student=student,
                is_present=True
            ).count()
            progress_data['attendance_rate'] = round((present_count / total_attendance) * 100, 2)
        
        return Response(progress_data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search students"""
        query = request.query_params.get('q', '')
        queryset = self.get_queryset()
        
        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(student_id__icontains=query) |
                Q(user__email__icontains=query)
            )
        
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    """Enrollment viewset"""
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Enrollment.objects.all()
        elif user.user_type == 'instructor':
            return Enrollment.objects.all()
        elif hasattr(user, 'student_profile'):
            return Enrollment.objects.filter(student=user.student_profile)
        else:
            return Enrollment.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin and instructors can modify enrollments
            if not self.request.user.user_type in ['admin', 'instructor']:
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark enrollment as completed"""
        enrollment = self.get_object()
        enrollment.status = 'completed'
        enrollment.save()
        
        return Response({'status': 'completed'})
    
    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get enrollment attendance"""
        enrollment = self.get_object()
        attendance = enrollment.attendances.all()
        
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def assessments(self, request, pk=None):
        """Get enrollment assessment results"""
        enrollment = self.get_object()
        results = enrollment.assessment_results.all()
        
        serializer = AssessmentResultSerializer(results, many=True)
        return Response(serializer.data)


class AttendanceViewSet(viewsets.ModelViewSet):
    """Attendance viewset"""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Attendance.objects.all()
        elif user.user_type == 'instructor':
            return Attendance.objects.all()
        elif hasattr(user, 'student_profile'):
            return Attendance.objects.filter(enrollment__student=user.student_profile)
        else:
            return Attendance.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin and instructors can modify attendance
            if not self.request.user.user_type in ['admin', 'instructor']:
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)


class AssessmentResultViewSet(viewsets.ModelViewSet):
    """Assessment result viewset"""
    queryset = AssessmentResult.objects.all()
    serializer_class = AssessmentResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return AssessmentResult.objects.all()
        elif user.user_type == 'instructor':
            return AssessmentResult.objects.all()
        elif hasattr(user, 'student_profile'):
            return AssessmentResult.objects.filter(enrollment__student=user.student_profile)
        else:
            return AssessmentResult.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin and instructors can modify assessment results
            if not self.request.user.user_type in ['admin', 'instructor']:
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(graded_by=self.request.user)


class ProgressReportViewSet(viewsets.ModelViewSet):
    """Progress report viewset"""
    queryset = ProgressReport.objects.all()
    serializer_class = ProgressReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return ProgressReport.objects.all()
        elif user.user_type == 'instructor':
            return ProgressReport.objects.all()
        elif hasattr(user, 'student_profile'):
            return ProgressReport.objects.filter(enrollment__student=user.student_profile)
        else:
            return ProgressReport.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin and instructors can modify progress reports
            if not self.request.user.user_type in ['admin', 'instructor']:
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PlacementViewSet(viewsets.ModelViewSet):
    """Placement viewset"""
    queryset = Placement.objects.all()
    serializer_class = PlacementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Placement.objects.all()
        elif hasattr(user, 'student_profile'):
            return Placement.objects.filter(student=user.student_profile)
        elif hasattr(user, 'employer_profile'):
            return Placement.objects.filter(employer=user.employer_profile)
        else:
            return Placement.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify placements
            if not self.request.user.user_type == 'admin':
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
