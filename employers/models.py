from django.db import models
from django.core.validators import RegexValidator
from accounts.models import User


class Employer(models.Model):
    """Employer profile extending User model"""
    COMPANY_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('family', 'Family'),
        ('company', 'Company'),
        ('agency', 'Agency'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=200)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES)
    registration_number = models.CharField(max_length=50, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    company_address = models.TextField()
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    contact_email = models.EmailField()
    business_description = models.TextField()
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.contact_person}"

    class Meta:
        verbose_name = "Employer"
        verbose_name_plural = "Employers"


class JobPosting(models.Model):
    """Job postings by employers"""
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('closed', 'Closed'),
        ('filled', 'Filled'),
    ]
    
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_postings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    duration_months = models.PositiveIntegerField(null=True, blank=True)
    required_skills = models.TextField()
    preferred_qualifications = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_urgent = models.BooleanField(default=False)
    application_deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.employer.company_name}"

    class Meta:
        verbose_name = "Job Posting"
        verbose_name_plural = "Job Postings"


class JobApplication(models.Model):
    """Applications for job postings"""
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('offered', 'Offered'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='job_applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    cover_letter = models.TextField(blank=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    availability_date = models.DateField()
    notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.job_posting.title}"

    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"
        unique_together = ['job_posting', 'student']


class EmployerFeedback(models.Model):
    """Feedback from employers about placed students"""
    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    ]
    
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='feedbacks')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='employer_feedbacks')
    placement = models.ForeignKey('students.Placement', on_delete=models.CASCADE, related_name='feedbacks')
    overall_rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    punctuality_rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    quality_rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    communication_rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    reliability_rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    would_rehire = models.BooleanField()
    additional_comments = models.TextField(blank=True)
    feedback_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.student.user.get_full_name()} from {self.employer.company_name}"

    class Meta:
        verbose_name = "Employer Feedback"
        verbose_name_plural = "Employer Feedbacks"


class RehireRequest(models.Model):
    """Requests from employers to rehire students"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='rehire_requests')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='rehire_requests')
    previous_placement = models.ForeignKey('students.Placement', on_delete=models.CASCADE, related_name='rehire_requests')
    new_job_title = models.CharField(max_length=200)
    new_salary = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    duration_months = models.PositiveIntegerField(null=True, blank=True)
    reason_for_rehire = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Rehire request for {self.student.user.get_full_name()} by {self.employer.company_name}"

    class Meta:
        verbose_name = "Rehire Request"
        verbose_name_plural = "Rehire Requests"