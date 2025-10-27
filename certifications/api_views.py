from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from .models import CertificateTemplate, Certificate, CertificateVerification, Accreditation, CourseAccreditation, CompetencyAssessment
from .serializers import (
    CertificateTemplateSerializer, CertificateSerializer, CertificateVerificationSerializer,
    AccreditationSerializer, CourseAccreditationSerializer, CompetencyAssessmentSerializer
)


class CertificateTemplateViewSet(viewsets.ModelViewSet):
    """Certificate template viewset"""
    queryset = CertificateTemplate.objects.filter(is_active=True)
    serializer_class = CertificateTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify templates
            if not self.request.user.user_type == 'admin':
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class CertificateViewSet(viewsets.ModelViewSet):
    """Certificate viewset"""
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Certificate.objects.all()
        elif hasattr(user, 'student_profile'):
            return Certificate.objects.filter(student=user.student_profile)
        else:
            return Certificate.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify certificates
            if not self.request.user.user_type == 'admin':
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download certificate"""
        certificate = self.get_object()
        
        if certificate.certificate_file:
            from django.http import HttpResponse
            response = HttpResponse(certificate.certificate_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{certificate.certificate_number}.pdf"'
            return response
        else:
            return Response({'error': 'Certificate file not available'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def verify(self, request):
        """Verify certificate by code"""
        verification_code = request.query_params.get('code')
        if not verification_code:
            return Response({'error': 'Verification code required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            certificate = Certificate.objects.get(verification_code=verification_code)
            serializer = CertificateSerializer(certificate)
            return Response(serializer.data)
        except Certificate.DoesNotExist:
            return Response({'error': 'Invalid verification code'}, status=status.HTTP_404_NOT_FOUND)


class CertificateVerificationViewSet(viewsets.ModelViewSet):
    """Certificate verification viewset"""
    queryset = CertificateVerification.objects.all()
    serializer_class = CertificateVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify verifications
            if not self.request.user.user_type == 'admin':
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class AccreditationViewSet(viewsets.ModelViewSet):
    """Accreditation viewset"""
    queryset = Accreditation.objects.filter(is_active=True)
    serializer_class = AccreditationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify accreditations
            if not self.request.user.user_type == 'admin':
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class CourseAccreditationViewSet(viewsets.ModelViewSet):
    """Course accreditation viewset"""
    queryset = CourseAccreditation.objects.filter(is_active=True)
    serializer_class = CourseAccreditationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify course accreditations
            if not self.request.user.user_type == 'admin':
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class CompetencyAssessmentViewSet(viewsets.ModelViewSet):
    """Competency assessment viewset"""
    queryset = CompetencyAssessment.objects.all()
    serializer_class = CompetencyAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return CompetencyAssessment.objects.all()
        elif hasattr(user, 'student_profile'):
            return CompetencyAssessment.objects.filter(student=user.student_profile)
        elif user.user_type == 'instructor':
            return CompetencyAssessment.objects.filter(assessor=user)
        else:
            return CompetencyAssessment.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin and instructors can modify assessments
            if not self.request.user.user_type in ['admin', 'instructor']:
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(assessor=self.request.user)
