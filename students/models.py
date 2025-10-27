from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from accounts.models import User
from courses.models import Course


class Student(models.Model):
    """Student profile extending User model"""
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    emergency_contact_relationship = models.CharField(max_length=50)
    education_level = models.CharField(max_length=100)
    previous_experience = models.TextField(blank=True)
    languages_spoken = models.CharField(max_length=200)
    special_skills = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Enrollment(models.Model):
    """Student enrollment in courses"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('suspended', 'Suspended'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    expected_completion_date = models.DateField()
    actual_completion_date = models.DateField(null=True, blank=True)
    tuition_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.title}"

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        unique_together = ['student', 'course']


class Attendance(models.Model):
    """Student attendance tracking"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    hours_attended = models.DecimalField(max_digits=4, decimal_places=2)
    is_present = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.enrollment.student.user.get_full_name()} - {self.date}"

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance Records"
        unique_together = ['enrollment', 'date']


class AssessmentResult(models.Model):
    """Student assessment results"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='assessment_results')
    assessment = models.ForeignKey('courses.Assessment', on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    max_score = models.PositiveIntegerField()
    passed = models.BooleanField()
    attempt_number = models.PositiveIntegerField(default=1)
    completed_date = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='graded_assessments')

    def __str__(self):
        return f"{self.enrollment.student.user.get_full_name()} - {self.assessment.title}"

    class Meta:
        verbose_name = "Assessment Result"
        verbose_name_plural = "Assessment Results"


class ProgressReport(models.Model):
    """Student progress reports"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='progress_reports')
    report_date = models.DateField()
    overall_progress = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2)
    average_score = models.DecimalField(max_digits=5, decimal_places=2)
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    recommendations = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.enrollment.student.user.get_full_name()} - Progress Report {self.report_date}"

    class Meta:
        verbose_name = "Progress Report"
        verbose_name_plural = "Progress Reports"


class Placement(models.Model):
    """Student placement/job assignments"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('placed', 'Placed'),
        ('completed', 'Completed'),
        ('terminated', 'Terminated'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='placements')
    employer = models.ForeignKey('employers.Employer', on_delete=models.CASCADE, related_name='placements')
    job_title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    placement_fee = models.DecimalField(max_digits=10, decimal_places=2)
    contract_document = models.FileField(upload_to='contracts/', blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.job_title} at {self.employer.company_name}"

    class Meta:
        verbose_name = "Placement"
        verbose_name_plural = "Placements"