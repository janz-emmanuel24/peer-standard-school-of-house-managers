from django.contrib import admin
from .models import Employer, JobPosting, JobApplication, EmployerFeedback, RehireRequest


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    """Employer admin"""
    list_display = ('company_name', 'company_type', 'contact_person', 'contact_phone', 'is_verified', 'is_active', 'registration_date')
    list_filter = ('company_type', 'is_verified', 'is_active', 'registration_date')
    search_fields = ('company_name', 'contact_person', 'contact_phone', 'contact_email')
    readonly_fields = ('registration_date',)
    
    fieldsets = (
        ('Company Information', {
            'fields': ('user', 'company_name', 'company_type', 'registration_number', 'tax_id', 'website')
        }),
        ('Contact Information', {
            'fields': ('company_address', 'contact_person', 'contact_phone', 'contact_email')
        }),
        ('Business Details', {
            'fields': ('business_description', 'is_verified', 'is_active', 'registration_date')
        }),
    )


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    """Job Posting admin"""
    list_display = ('title', 'employer', 'employment_type', 'salary_min', 'salary_max', 'location', 'status', 'created_at')
    list_filter = ('status', 'employment_type', 'is_urgent', 'created_at')
    search_fields = ('title', 'description', 'requirements', 'location')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Job Details', {
            'fields': ('employer', 'title', 'description', 'requirements', 'responsibilities')
        }),
        ('Employment Terms', {
            'fields': ('employment_type', 'salary_min', 'salary_max', 'location', 'start_date', 'duration_months')
        }),
        ('Requirements & Benefits', {
            'fields': ('required_skills', 'preferred_qualifications', 'benefits')
        }),
        ('Status & Dates', {
            'fields': ('status', 'is_urgent', 'application_deadline', 'created_at', 'updated_at')
        }),
    )


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    """Job Application admin"""
    list_display = ('student', 'job_posting', 'status', 'expected_salary', 'availability_date', 'applied_at')
    list_filter = ('status', 'applied_at', 'availability_date')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'job_posting__title')
    readonly_fields = ('applied_at', 'updated_at')


@admin.register(EmployerFeedback)
class EmployerFeedbackAdmin(admin.ModelAdmin):
    """Employer Feedback admin"""
    list_display = ('employer', 'student', 'overall_rating', 'would_rehire', 'feedback_date')
    list_filter = ('overall_rating', 'would_rehire', 'feedback_date')
    search_fields = ('employer__company_name', 'student__user__first_name', 'student__user__last_name')
    readonly_fields = ('feedback_date',)
    
    fieldsets = (
        ('Feedback Details', {
            'fields': ('employer', 'student', 'placement')
        }),
        ('Ratings', {
            'fields': ('overall_rating', 'punctuality_rating', 'quality_rating', 'communication_rating', 'reliability_rating')
        }),
        ('Comments', {
            'fields': ('strengths', 'areas_for_improvement', 'additional_comments')
        }),
        ('Decision', {
            'fields': ('would_rehire', 'feedback_date')
        }),
    )


@admin.register(RehireRequest)
class RehireRequestAdmin(admin.ModelAdmin):
    """Rehire Request admin"""
    list_display = ('employer', 'student', 'new_job_title', 'new_salary', 'start_date', 'status', 'requested_at')
    list_filter = ('status', 'requested_at', 'start_date')
    search_fields = ('employer__company_name', 'student__user__first_name', 'student__user__last_name', 'new_job_title')
    readonly_fields = ('requested_at', 'approved_at')
    
    fieldsets = (
        ('Request Details', {
            'fields': ('employer', 'student', 'previous_placement')
        }),
        ('New Position', {
            'fields': ('new_job_title', 'new_salary', 'start_date', 'duration_months')
        }),
        ('Reason & Status', {
            'fields': ('reason_for_rehire', 'status', 'approved_by', 'requested_at', 'approved_at')
        }),
    )