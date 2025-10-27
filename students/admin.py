from django.contrib import admin
from .models import Student, Enrollment, Attendance, AssessmentResult, ProgressReport, Placement


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Student admin"""
    list_display = ('user', 'student_id', 'gender', 'marital_status', 'education_level', 'is_active', 'enrollment_date')
    list_filter = ('gender', 'marital_status', 'is_active', 'enrollment_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'student_id')
    readonly_fields = ('enrollment_date',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'student_id', 'gender', 'marital_status')
        }),
        ('Contact Information', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Education & Experience', {
            'fields': ('education_level', 'previous_experience', 'languages_spoken', 'special_skills')
        }),
        ('Additional Information', {
            'fields': ('medical_conditions', 'is_active', 'enrollment_date')
        }),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Enrollment admin"""
    list_display = ('student', 'course', 'status', 'enrollment_date', 'start_date', 'expected_completion_date')
    list_filter = ('status', 'enrollment_date', 'start_date', 'course')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'course__title')
    readonly_fields = ('enrollment_date',)
    
    fieldsets = (
        ('Enrollment Details', {
            'fields': ('student', 'course', 'status', 'enrollment_date')
        }),
        ('Dates', {
            'fields': ('start_date', 'expected_completion_date', 'actual_completion_date')
        }),
        ('Financial', {
            'fields': ('tuition_paid',)
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """Attendance admin"""
    list_display = ('enrollment', 'date', 'hours_attended', 'is_present', 'recorded_by')
    list_filter = ('is_present', 'date', 'recorded_by')
    search_fields = ('enrollment__student__user__first_name', 'enrollment__student__user__last_name')
    date_hierarchy = 'date'


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    """Assessment Result admin"""
    list_display = ('enrollment', 'assessment', 'score', 'max_score', 'passed', 'attempt_number', 'completed_date')
    list_filter = ('passed', 'attempt_number', 'completed_date', 'assessment')
    search_fields = ('enrollment__student__user__first_name', 'enrollment__student__user__last_name', 'assessment__title')
    readonly_fields = ('completed_date',)


@admin.register(ProgressReport)
class ProgressReportAdmin(admin.ModelAdmin):
    """Progress Report admin"""
    list_display = ('enrollment', 'report_date', 'overall_progress', 'attendance_rate', 'average_score', 'created_by')
    list_filter = ('report_date', 'created_by')
    search_fields = ('enrollment__student__user__first_name', 'enrollment__student__user__last_name')
    date_hierarchy = 'report_date'


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    """Placement admin"""
    list_display = ('student', 'employer', 'job_title', 'start_date', 'end_date', 'salary', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'employer__company_name', 'job_title')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Placement Details', {
            'fields': ('student', 'employer', 'job_title', 'status')
        }),
        ('Dates & Compensation', {
            'fields': ('start_date', 'end_date', 'salary', 'placement_fee')
        }),
        ('Documents', {
            'fields': ('contract_document',)
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_at')
        }),
    )