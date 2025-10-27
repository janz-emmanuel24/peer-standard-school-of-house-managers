from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Extended User model with additional fields for different user types"""
    USER_TYPE_CHOICES = [
        ('admin', 'Administrator'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
        ('employer', 'Employer'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")],
        blank=True
    )
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class BackgroundCheck(models.Model):
    """Model for background verification of users"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='background_checks')
    check_type = models.CharField(max_length=50)  # e.g., 'criminal', 'employment', 'education'
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verification_agency = models.CharField(max_length=100)
    reference_number = models.CharField(max_length=50, unique=True)
    conducted_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    documents = models.FileField(upload_to='background_checks/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.check_type} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Background Check"
        verbose_name_plural = "Background Checks"