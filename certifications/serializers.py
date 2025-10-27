from rest_framework import serializers
from .models import CertificateTemplate, Certificate, CertificateVerification, Accreditation, CourseAccreditation, CompetencyAssessment


class CertificateTemplateSerializer(serializers.ModelSerializer):
    """Certificate template serializer"""
    class Meta:
        model = CertificateTemplate
        fields = ['id', 'name', 'description', 'template_file', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class CertificateSerializer(serializers.ModelSerializer):
    """Certificate serializer"""
    student_name = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    template_name = serializers.SerializerMethodField()
    issued_by_name = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    verification_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Certificate
        fields = [
            'id', 'student', 'student_name', 'course', 'course_title', 
            'certificate_number', 'template', 'template_name', 'status', 
            'issue_date', 'expiry_date', 'final_grade', 'overall_score', 
            'certificate_file', 'verification_code', 'verification_url',
            'notes', 'issued_by', 'issued_by_name', 'is_expired', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    
    def get_course_title(self, obj):
        return obj.course.title
    
    def get_template_name(self, obj):
        return obj.template.name if obj.template else None
    
    def get_issued_by_name(self, obj):
        return obj.issued_by.get_full_name()
    
    def get_is_expired(self, obj):
        if obj.expiry_date:
            from django.utils import timezone
            return timezone.now().date() > obj.expiry_date
        return False
    
    def get_verification_url(self, obj):
        return f"/certifications/verify/?code={obj.verification_code}"


class CertificateVerificationSerializer(serializers.ModelSerializer):
    """Certificate verification serializer"""
    certificate_number = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    
    class Meta:
        model = CertificateVerification
        fields = [
            'id', 'certificate', 'certificate_number', 'student_name', 
            'course_title', 'verified_by', 'verification_date', 
            'verification_purpose', 'is_valid', 'notes'
        ]
        read_only_fields = ['id', 'verification_date']
    
    def get_certificate_number(self, obj):
        return obj.certificate.certificate_number
    
    def get_student_name(self, obj):
        return obj.certificate.student.user.get_full_name()
    
    def get_course_title(self, obj):
        return obj.certificate.course.title


class AccreditationSerializer(serializers.ModelSerializer):
    """Accreditation serializer"""
    is_expired = serializers.SerializerMethodField()
    course_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Accreditation
        fields = [
            'id', 'name', 'description', 'accreditation_body', 
            'accreditation_number', 'issue_date', 'expiry_date', 'scope', 
            'is_active', 'certificate_file', 'is_expired', 'course_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_is_expired(self, obj):
        from django.utils import timezone
        return timezone.now().date() > obj.expiry_date
    
    def get_course_count(self, obj):
        return obj.courseaccreditation_set.filter(is_active=True).count()


class CourseAccreditationSerializer(serializers.ModelSerializer):
    """Course accreditation serializer"""
    course_title = serializers.SerializerMethodField()
    accreditation_name = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = CourseAccreditation
        fields = [
            'id', 'course', 'course_title', 'accreditation', 'accreditation_name', 
            'accredited_date', 'expiry_date', 'is_active', 'is_expired'
        ]
        read_only_fields = ['id']
    
    def get_course_title(self, obj):
        return obj.course.title
    
    def get_accreditation_name(self, obj):
        return obj.accreditation.name
    
    def get_is_expired(self, obj):
        from django.utils import timezone
        return timezone.now().date() > obj.expiry_date


class CompetencyAssessmentSerializer(serializers.ModelSerializer):
    """Competency assessment serializer"""
    student_name = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    assessor_name = serializers.SerializerMethodField()
    retraining_course_titles = serializers.SerializerMethodField()
    
    class Meta:
        model = CompetencyAssessment
        fields = [
            'id', 'student', 'student_name', 'course', 'course_title', 
            'assessment_type', 'assessment_date', 'assessor', 'assessor_name', 
            'overall_score', 'passed', 'areas_assessed', 'strengths', 
            'areas_for_improvement', 'recommendations', 'requires_retraining', 
            'retraining_courses', 'retraining_course_titles', 'next_assessment_date', 
            'notes'
        ]
        read_only_fields = ['id']
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    
    def get_course_title(self, obj):
        return obj.course.title
    
    def get_assessor_name(self, obj):
        return obj.assessor.get_full_name()
    
    def get_retraining_course_titles(self, obj):
        return [course.title for course in obj.retraining_courses.all()]
