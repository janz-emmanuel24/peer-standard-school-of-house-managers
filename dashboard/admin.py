from django.contrib import admin
from .models import DashboardWidget, UserDashboard, SystemNotification, AuditLog, SystemSetting


@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    """Dashboard Widget admin"""
    list_display = ('name', 'widget_type', 'title', 'is_active', 'order')
    list_filter = ('widget_type', 'is_active')
    search_fields = ('name', 'title', 'description')
    ordering = ('order',)


@admin.register(UserDashboard)
class UserDashboardAdmin(admin.ModelAdmin):
    """User Dashboard admin"""
    list_display = ('user', 'updated_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('updated_at',)


@admin.register(SystemNotification)
class SystemNotificationAdmin(admin.ModelAdmin):
    """System Notification admin"""
    list_display = ('title', 'priority', 'is_active', 'start_date', 'end_date', 'created_by')
    list_filter = ('priority', 'is_active', 'start_date', 'end_date', 'created_by')
    search_fields = ('title', 'message')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('title', 'message', 'priority')
        }),
        ('Targeting', {
            'fields': ('target_users',)
        }),
        ('Schedule', {
            'fields': ('is_active', 'start_date', 'end_date')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at')
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Audit Log admin"""
    list_display = ('user', 'action', 'model_name', 'object_id', 'timestamp', 'ip_address')
    list_filter = ('action', 'model_name', 'timestamp')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'description', 'object_id')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Action Details', {
            'fields': ('user', 'action', 'model_name', 'object_id', 'description')
        }),
        ('Technical Information', {
            'fields': ('ip_address', 'user_agent', 'timestamp')
        }),
    )


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    """System Setting admin"""
    list_display = ('key', 'value', 'setting_type', 'is_encrypted', 'updated_by', 'updated_at')
    list_filter = ('setting_type', 'is_encrypted', 'updated_at')
    search_fields = ('key', 'value', 'description')
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('Setting Information', {
            'fields': ('key', 'value', 'setting_type', 'description')
        }),
        ('Security', {
            'fields': ('is_encrypted',)
        }),
        ('Metadata', {
            'fields': ('updated_by', 'updated_at')
        }),
    )