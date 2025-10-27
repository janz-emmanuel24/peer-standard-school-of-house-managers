from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, BackgroundCheck


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_verified', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('user_type', 'phone_number', 'address', 'date_of_birth', 'profile_picture', 'is_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('user_type', 'phone_number', 'address', 'date_of_birth', 'profile_picture', 'is_verified')
        }),
    )


@admin.register(BackgroundCheck)
class BackgroundCheckAdmin(admin.ModelAdmin):
    """Background Check admin"""
    list_display = ('user', 'check_type', 'status', 'verification_agency', 'conducted_date', 'expiry_date')
    list_filter = ('status', 'check_type', 'verification_agency', 'conducted_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'reference_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'check_type', 'verification_agency', 'reference_number')
        }),
        ('Status & Dates', {
            'fields': ('status', 'conducted_date', 'expiry_date')
        }),
        ('Additional Information', {
            'fields': ('notes', 'documents')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )