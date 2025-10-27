from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User


class CourseCategory(models.Model):
    """Categories for organizing courses"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Course Category"
        verbose_name_plural = "Course Categories"


class Course(models.Model):
    """Training courses/modules"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('retired', 'Retired'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='courses')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    duration_weeks = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(52)])
    total_hours = models.PositiveIntegerField()
    max_students = models.PositiveIntegerField(default=30)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    learning_outcomes = models.TextField()
    course_materials = models.FileField(upload_to='course_materials/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class CourseModule(models.Model):
    """Individual modules within a course"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField()
    duration_hours = models.PositiveIntegerField()
    content = models.TextField()
    is_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        verbose_name = "Course Module"
        verbose_name_plural = "Course Modules"
        ordering = ['course', 'order']


class Instructor(models.Model):
    """Instructors who teach courses"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    specialization = models.CharField(max_length=200)
    years_experience = models.PositiveIntegerField()
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    bio = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"

    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = "Instructors"


class CourseInstructor(models.Model):
    """Many-to-many relationship between courses and instructors"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.instructor.user.get_full_name()}"

    class Meta:
        verbose_name = "Course Instructor"
        verbose_name_plural = "Course Instructors"
        unique_together = ['course', 'instructor']


class Assessment(models.Model):
    """Assessments for courses"""
    ASSESSMENT_TYPE_CHOICES = [
        ('quiz', 'Quiz'),
        ('practical', 'Practical'),
        ('assignment', 'Assignment'),
        ('final_exam', 'Final Exam'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assessments')
    title = models.CharField(max_length=200)
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPE_CHOICES)
    description = models.TextField()
    max_score = models.PositiveIntegerField(default=100)
    passing_score = models.PositiveIntegerField(default=70)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    instructions = models.TextField()
    is_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"