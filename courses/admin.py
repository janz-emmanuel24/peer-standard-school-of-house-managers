from django.contrib import admin
from .models import CourseCategory, Course, CourseModule, Instructor, CourseInstructor, Assessment


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    """Course Category admin"""
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Course admin"""
    list_display = ('title', 'category', 'difficulty_level', 'duration_weeks', 'tuition_fee', 'status', 'created_by')
    list_filter = ('status', 'difficulty_level', 'category', 'created_at')
    search_fields = ('title', 'description', 'learning_outcomes')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'difficulty_level')
        }),
        ('Course Details', {
            'fields': ('duration_weeks', 'total_hours', 'max_students', 'tuition_fee')
        }),
        ('Content', {
            'fields': ('learning_outcomes', 'prerequisites', 'course_materials')
        }),
        ('Status & Metadata', {
            'fields': ('status', 'created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    """Course Module admin"""
    list_display = ('title', 'course', 'order', 'duration_hours', 'is_required')
    list_filter = ('is_required', 'course', 'created_at')
    search_fields = ('title', 'description', 'content')
    ordering = ('course', 'order')


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    """Instructor admin"""
    list_display = ('user', 'employee_id', 'specialization', 'years_experience', 'hourly_rate', 'is_active')
    list_filter = ('is_active', 'specialization', 'years_experience')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id', 'specialization')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'employee_id', 'specialization')
        }),
        ('Experience & Rates', {
            'fields': ('years_experience', 'hourly_rate')
        }),
        ('Additional Information', {
            'fields': ('bio', 'certifications', 'is_active')
        }),
    )


@admin.register(CourseInstructor)
class CourseInstructorAdmin(admin.ModelAdmin):
    """Course Instructor admin"""
    list_display = ('course', 'instructor', 'is_primary', 'assigned_date')
    list_filter = ('is_primary', 'assigned_date')
    search_fields = ('course__title', 'instructor__user__first_name', 'instructor__user__last_name')


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    """Assessment admin"""
    list_display = ('title', 'course', 'assessment_type', 'max_score', 'passing_score', 'is_required')
    list_filter = ('assessment_type', 'is_required', 'course')
    search_fields = ('title', 'description', 'instructions')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'title', 'assessment_type', 'description')
        }),
        ('Scoring', {
            'fields': ('max_score', 'passing_score')
        }),
        ('Details', {
            'fields': ('duration_minutes', 'instructions', 'is_required')
        }),
    )