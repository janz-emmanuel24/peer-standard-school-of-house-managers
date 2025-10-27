from django.db import models
from accounts.models import User


class DashboardWidget(models.Model):
    """Customizable dashboard widgets"""
    WIDGET_TYPE_CHOICES = [
        ('chart', 'Chart'),
        ('table', 'Table'),
        ('metric', 'Metric'),
        ('list', 'List'),
        ('calendar', 'Calendar'),
    ]
    
    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    data_source = models.CharField(max_length=100)  # Model or function name
    configuration = models.JSONField(default=dict)  # Widget-specific settings
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Dashboard Widget"
        verbose_name_plural = "Dashboard Widgets"
        ordering = ['order']


class UserDashboard(models.Model):
    """User-specific dashboard configurations"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_config')
    widgets = models.ManyToManyField(DashboardWidget, blank=True)
    layout_config = models.JSONField(default=dict)  # Store layout preferences
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dashboard for {self.user.get_full_name()}"

    class Meta:
        verbose_name = "User Dashboard"
        verbose_name_plural = "User Dashboards"


class SystemNotification(models.Model):
    """System-wide notifications"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    target_users = models.ManyToManyField(User, blank=True)  # If empty, show to all users
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notifications')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "System Notification"
        verbose_name_plural = "System Notifications"


class AuditLog(models.Model):
    """System audit trail"""
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view', 'View'),
        ('export', 'Export'),
        ('import', 'Import'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_action_display()} {self.model_name}"

    class Meta:
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        ordering = ['-timestamp']


class SystemSetting(models.Model):
    """System configuration settings"""
    SETTING_TYPE_CHOICES = [
        ('general', 'General'),
        ('academic', 'Academic'),
        ('financial', 'Financial'),
        ('notification', 'Notification'),
        ('security', 'Security'),
    ]
    
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    setting_type = models.CharField(max_length=20, choices=SETTING_TYPE_CHOICES)
    description = models.TextField(blank=True)
    is_encrypted = models.BooleanField(default=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_settings')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.key} = {self.value}"

    class Meta:
        verbose_name = "System Setting"
        verbose_name_plural = "System Settings"