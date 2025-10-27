from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from .models import Employer, JobPosting, JobApplication, EmployerFeedback, RehireRequest
from .serializers import (
    EmployerSerializer, JobPostingSerializer, JobApplicationSerializer,
    EmployerFeedbackSerializer, RehireRequestSerializer
)


class EmployerViewSet(viewsets.ModelViewSet):
    """Employer viewset"""
    queryset = Employer.objects.filter(is_active=True)
    serializer_class = EmployerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Employer.objects.all()
        elif hasattr(user, 'employer_profile'):
            return Employer.objects.filter(id=user.employer_profile.id)
        else:
            return Employer.objects.filter(is_active=True)
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify employers
            if not (self.request.user.is_authenticated and self.request.user.user_type == 'admin'):
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def job_postings(self, request, pk=None):
        """Get employer's job postings"""
        employer = self.get_object()
        jobs = employer.job_postings.all()
        
        serializer = JobPostingSerializer(jobs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def placements(self, request, pk=None):
        """Get employer's placements"""
        employer = self.get_object()
        placements = employer.placements.all()
        
        from students.serializers import PlacementSerializer
        serializer = PlacementSerializer(placements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search employers"""
        query = request.query_params.get('q', '')
        queryset = self.get_queryset()
        
        if query:
            queryset = queryset.filter(
                Q(company_name__icontains=query) |
                Q(contact_person__icontains=query) |
                Q(business_description__icontains=query)
            )
        
        serializer = EmployerSerializer(queryset, many=True)
        return Response(serializer.data)


class JobPostingViewSet(viewsets.ModelViewSet):
    """Job posting viewset"""
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = JobPosting.objects.all()
        status_filter = self.request.query_params.get('status', None)
        employer = self.request.query_params.get('employer', None)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if employer:
            queryset = queryset.filter(employer_id=employer)
        
        return queryset.select_related('employer')
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin and employers can modify job postings
            if not self.request.user.user_type in ['admin', 'employer']:
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """Get job posting applications"""
        job = self.get_object()
        applications = job.applications.select_related('student__user').all()
        
        serializer = JobApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        """Apply for a job posting"""
        if not hasattr(request.user, 'student_profile'):
            return Response({'error': 'Student profile required'}, status=status.HTTP_400_BAD_REQUEST)
        
        job = self.get_object()
        student = request.user.student_profile
        
        # Check if already applied
        if JobApplication.objects.filter(job_posting=job, student=student).exists():
            return Response({'error': 'Already applied for this job'}, status=status.HTTP_400_BAD_REQUEST)
        
        application = JobApplication.objects.create(
            job_posting=job,
            student=student,
            cover_letter=request.data.get('cover_letter', ''),
            expected_salary=request.data.get('expected_salary'),
            availability_date=request.data.get('availability_date')
        )
        
        serializer = JobApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search job postings"""
        query = request.query_params.get('q', '')
        queryset = self.get_queryset()
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query) |
                Q(required_skills__icontains=query)
            )
        
        serializer = JobPostingSerializer(queryset, many=True)
        return Response(serializer.data)


class JobApplicationViewSet(viewsets.ModelViewSet):
    """Job application viewset"""
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return JobApplication.objects.all()
        elif hasattr(user, 'student_profile'):
            return JobApplication.objects.filter(student=user.student_profile)
        elif hasattr(user, 'employer_profile'):
            return JobApplication.objects.filter(job_posting__employer=user.employer_profile)
        else:
            return JobApplication.objects.none()
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin and employers can modify applications
            if not self.request.user.user_type in ['admin', 'employer']:
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve job application"""
        application = self.get_object()
        application.status = 'accepted'
        application.save()
        
        return Response({'status': 'approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject job application"""
        application = self.get_object()
        application.status = 'rejected'
        application.save()
        
        return Response({'status': 'rejected'})


class EmployerFeedbackViewSet(viewsets.ModelViewSet):
    """Employer feedback viewset"""
    queryset = EmployerFeedback.objects.all()
    serializer_class = EmployerFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return EmployerFeedback.objects.all()
        elif hasattr(user, 'employer_profile'):
            return EmployerFeedback.objects.filter(employer=user.employer_profile)
        elif hasattr(user, 'student_profile'):
            return EmployerFeedback.objects.filter(student=user.student_profile)
        else:
            return EmployerFeedback.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin and employers can modify feedback
            if not self.request.user.user_type in ['admin', 'employer']:
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.employer_profile)


class RehireRequestViewSet(viewsets.ModelViewSet):
    """Rehire request viewset"""
    queryset = RehireRequest.objects.all()
    serializer_class = RehireRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return RehireRequest.objects.all()
        elif hasattr(user, 'employer_profile'):
            return RehireRequest.objects.filter(employer=user.employer_profile)
        elif hasattr(user, 'student_profile'):
            return RehireRequest.objects.filter(student=user.student_profile)
        else:
            return RehireRequest.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin and employers can modify rehire requests
            if not self.request.user.user_type in ['admin', 'employer']:
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.employer_profile)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve rehire request (admin only)"""
        if request.user.user_type != 'admin':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        rehire_request = self.get_object()
        rehire_request.status = 'approved'
        rehire_request.approved_by = request.user
        rehire_request.save()
        
        return Response({'status': 'approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject rehire request (admin only)"""
        if request.user.user_type != 'admin':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        rehire_request = self.get_object()
        rehire_request.status = 'rejected'
        rehire_request.approved_by = request.user
        rehire_request.save()
        
        return Response({'status': 'rejected'})
