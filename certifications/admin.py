from django.contrib import admin
from .models import CertificateTemplate, Certificate, CertificateVerification, Accreditation, CourseAccreditation, CompetencyAssessment


@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    """Certificate Template admin"""
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    """Certificate admin"""
    list_display = ('student', 'course', 'certificate_number', 'status', 'issue_date', 'final_grade', 'overall_score')
    list_filter = ('status', 'issue_date', 'course')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'certificate_number', 'verification_code')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Certificate Details', {
            'fields': ('student', 'course', 'certificate_number', 'template', 'status')
        }),
        ('Dates & Grades', {
            'fields': ('issue_date', 'expiry_date', 'final_grade', 'overall_score')
        }),
        ('Verification', {
            'fields': ('verification_code', 'certificate_file')
        }),
        ('Additional Information', {
            'fields': ('notes', 'issued_by', 'created_at')
        }),
    )


@admin.register(CertificateVerification)
class CertificateVerificationAdmin(admin.ModelAdmin):
    """Certificate Verification admin"""
    list_display = ('certificate', 'verified_by', 'verification_date', 'is_valid')
    list_filter = ('is_valid', 'verification_date')
    search_fields = ('certificate__certificate_number', 'verified_by', 'verification_purpose')
    readonly_fields = ('verification_date',)


@admin.register(Accreditation)
class AccreditationAdmin(admin.ModelAdmin):
    """Accreditation admin"""
    list_display = ('name', 'accreditation_body', 'accreditation_number', 'issue_date', 'expiry_date', 'is_active')
    list_filter = ('is_active', 'issue_date', 'expiry_date')
    search_fields = ('name', 'accreditation_body', 'accreditation_number')
    readonly_fields = ('created_at',)


@admin.register(CourseAccreditation)
class CourseAccreditationAdmin(admin.ModelAdmin):
    """Course Accreditation admin"""
    list_display = ('course', 'accreditation', 'accredited_date', 'expiry_date', 'is_active')
    list_filter = ('is_active', 'accredited_date', 'expiry_date')
    search_fields = ('course__title', 'accreditation__name')


@admin.register(CompetencyAssessment)
class CompetencyAssessmentAdmin(admin.ModelAdmin):
    """Competency Assessment admin"""
    list_display = ('student', 'course', 'assessment_type', 'assessment_date', 'overall_score', 'passed', 'requires_retraining')
    list_filter = ('assessment_type', 'passed', 'requires_retraining', 'assessment_date')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'course__title')
    
    fieldsets = (
        ('Assessment Details', {
            'fields': ('student', 'course', 'assessment_type', 'assessment_date', 'assessor')
        }),
        ('Results', {
            'fields': ('overall_score', 'passed', 'areas_assessed')
        }),
        ('Evaluation', {
            'fields': ('strengths', 'areas_for_improvement', 'recommendations')
        }),
        ('Retraining', {
            'fields': ('requires_retraining', 'retraining_courses', 'next_assessment_date')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )