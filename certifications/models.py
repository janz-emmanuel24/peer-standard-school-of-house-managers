from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from students.models import Student
from courses.models import Course


class CertificateTemplate(models.Model):
    """Templates for generating certificates"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    template_file = models.FileField(upload_to='certificate_templates/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Certificate Template"
        verbose_name_plural = "Certificate Templates"


class Certificate(models.Model):
    """Generated certificates for students"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('issued', 'Issued'),
        ('verified', 'Verified'),
        ('revoked', 'Revoked'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    certificate_number = models.CharField(max_length=50, unique=True)
    template = models.ForeignKey(CertificateTemplate, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    final_grade = models.CharField(max_length=10)
    overall_score = models.DecimalField(max_digits=5, decimal_places=2)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    verification_code = models.CharField(max_length=20, unique=True)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_certificates')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.title} ({self.certificate_number})"

    class Meta:
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"


class CertificateVerification(models.Model):
    """Certificate verification records"""
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, related_name='verifications')
    verified_by = models.CharField(max_length=200)  # Name of person/entity verifying
    verification_date = models.DateTimeField(auto_now_add=True)
    verification_purpose = models.CharField(max_length=200)
    is_valid = models.BooleanField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Verification of {self.certificate.certificate_number} by {self.verified_by}"

    class Meta:
        verbose_name = "Certificate Verification"
        verbose_name_plural = "Certificate Verifications"


class Accreditation(models.Model):
    """Accreditation bodies and standards"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    accreditation_body = models.CharField(max_length=200)
    accreditation_number = models.CharField(max_length=100, unique=True)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    scope = models.TextField()
    is_active = models.BooleanField(default=True)
    certificate_file = models.FileField(upload_to='accreditations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.accreditation_body}"

    class Meta:
        verbose_name = "Accreditation"
        verbose_name_plural = "Accreditations"


class CourseAccreditation(models.Model):
    """Accreditation of specific courses"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='accreditations')
    accreditation = models.ForeignKey(Accreditation, on_delete=models.CASCADE, related_name='courses')
    accredited_date = models.DateField()
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course.title} - {self.accreditation.name}"

    class Meta:
        verbose_name = "Course Accreditation"
        verbose_name_plural = "Course Accreditations"
        unique_together = ['course', 'accreditation']


class CompetencyAssessment(models.Model):
    """Competency assessments for re-training"""
    ASSESSMENT_TYPE_CHOICES = [
        ('initial', 'Initial Assessment'),
        ('periodic', 'Periodic Assessment'),
        ('renewal', 'Renewal Assessment'),
        ('upgrade', 'Upgrade Assessment'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='competency_assessments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='competency_assessments')
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPE_CHOICES)
    assessment_date = models.DateField()
    assessor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conducted_assessments')
    overall_score = models.DecimalField(max_digits=5, decimal_places=2)
    passed = models.BooleanField()
    areas_assessed = models.TextField()
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    recommendations = models.TextField()
    requires_retraining = models.BooleanField(default=False)
    retraining_courses = models.ManyToManyField(Course, blank=True, related_name='retraining_assessments')
    next_assessment_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.title} ({self.get_assessment_type_display()})"

    class Meta:
        verbose_name = "Competency Assessment"
        verbose_name_plural = "Competency Assessments"