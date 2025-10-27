from rest_framework import serializers
from .models import Employer, JobPosting, JobApplication, EmployerFeedback, RehireRequest


class EmployerSerializer(serializers.ModelSerializer):
    """Employer serializer"""
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    job_count = serializers.SerializerMethodField()
    placement_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Employer
        fields = [
            'id', 'user', 'full_name', 'email', 'phone_number', 'company_name', 
            'company_type', 'registration_number', 'tax_id', 'website', 
            'company_address', 'contact_person', 'contact_phone', 'contact_email', 
            'business_description', 'is_verified', 'is_active', 'registration_date',
            'job_count', 'placement_count'
        ]
        read_only_fields = ['id', 'registration_date']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    
    def get_email(self, obj):
        return obj.user.email
    
    def get_phone_number(self, obj):
        return obj.user.phone_number
    
    def get_job_count(self, obj):
        return obj.job_postings.count()
    
    def get_placement_count(self, obj):
        return obj.placements.count()


class JobPostingSerializer(serializers.ModelSerializer):
    """Job posting serializer"""
    employer_name = serializers.SerializerMethodField()
    application_count = serializers.SerializerMethodField()
    days_since_posted = serializers.SerializerMethodField()
    
    class Meta:
        model = JobPosting
        fields = [
            'id', 'employer', 'employer_name', 'title', 'description', 
            'requirements', 'responsibilities', 'employment_type', 'salary_min', 
            'salary_max', 'location', 'start_date', 'duration_months', 
            'required_skills', 'preferred_qualifications', 'benefits', 'status', 
            'is_urgent', 'application_deadline', 'application_count', 
            'days_since_posted', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_employer_name(self, obj):
        return obj.employer.company_name
    
    def get_application_count(self, obj):
        return obj.applications.count()
    
    def get_days_since_posted(self, obj):
        from django.utils import timezone
        return (timezone.now().date() - obj.created_at.date()).days


class JobApplicationSerializer(serializers.ModelSerializer):
    """Job application serializer"""
    student_name = serializers.SerializerMethodField()
    job_title = serializers.SerializerMethodField()
    employer_name = serializers.SerializerMethodField()
    days_since_applied = serializers.SerializerMethodField()
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'job_posting', 'job_title', 'employer_name', 'student', 
            'student_name', 'status', 'cover_letter', 'expected_salary', 
            'availability_date', 'notes', 'days_since_applied', 'applied_at', 'updated_at'
        ]
        read_only_fields = ['id', 'applied_at', 'updated_at']
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    
    def get_job_title(self, obj):
        return obj.job_posting.title
    
    def get_employer_name(self, obj):
        return obj.job_posting.employer.company_name
    
    def get_days_since_applied(self, obj):
        from django.utils import timezone
        return (timezone.now().date() - obj.applied_at.date()).days


class EmployerFeedbackSerializer(serializers.ModelSerializer):
    """Employer feedback serializer"""
    employer_name = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    job_title = serializers.SerializerMethodField()
    overall_rating_display = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployerFeedback
        fields = [
            'id', 'employer', 'employer_name', 'student', 'student_name', 
            'placement', 'job_title', 'overall_rating', 'overall_rating_display',
            'punctuality_rating', 'quality_rating', 'communication_rating', 
            'reliability_rating', 'strengths', 'areas_for_improvement', 
            'would_rehire', 'additional_comments', 'feedback_date'
        ]
        read_only_fields = ['id', 'feedback_date']
    
    def get_employer_name(self, obj):
        return obj.employer.company_name
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    
    def get_job_title(self, obj):
        return obj.placement.job_title
    
    def get_overall_rating_display(self, obj):
        return obj.get_overall_rating_display()


class RehireRequestSerializer(serializers.ModelSerializer):
    """Rehire request serializer"""
    employer_name = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    previous_job_title = serializers.SerializerMethodField()
    approved_by_name = serializers.SerializerMethodField()
    days_since_requested = serializers.SerializerMethodField()
    
    class Meta:
        model = RehireRequest
        fields = [
            'id', 'employer', 'employer_name', 'student', 'student_name', 
            'previous_placement', 'previous_job_title', 'new_job_title', 
            'new_salary', 'start_date', 'duration_months', 'reason_for_rehire', 
            'status', 'approved_by', 'approved_by_name', 'requested_at', 
            'approved_at', 'days_since_requested'
        ]
        read_only_fields = ['id', 'requested_at', 'approved_at']
    
    def get_employer_name(self, obj):
        return obj.employer.company_name
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    
    def get_previous_job_title(self, obj):
        return obj.previous_placement.job_title
    
    def get_approved_by_name(self, obj):
        return obj.approved_by.get_full_name() if obj.approved_by else None
    
    def get_days_since_requested(self, obj):
        from django.utils import timezone
        return (timezone.now().date() - obj.requested_at.date()).days
