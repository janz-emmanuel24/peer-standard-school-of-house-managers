from rest_framework import serializers
from .models import Student, Enrollment, Attendance, AssessmentResult, ProgressReport, Placement


class StudentSerializer(serializers.ModelSerializer):
    """Student serializer"""
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    date_of_birth = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    enrollment_count = serializers.SerializerMethodField()
    certificate_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'user', 'student_id', 'full_name', 'email', 'phone_number', 
            'address', 'date_of_birth', 'profile_picture', 'gender', 
            'marital_status', 'emergency_contact_name', 'emergency_contact_phone', 
            'emergency_contact_relationship', 'education_level', 
            'previous_experience', 'languages_spoken', 'special_skills', 
            'medical_conditions', 'is_active', 'enrollment_date', 
            'enrollment_count', 'certificate_count'
        ]
        read_only_fields = ['id', 'enrollment_date']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    
    def get_email(self, obj):
        return obj.user.email
    
    def get_phone_number(self, obj):
        return obj.user.phone_number
    
    def get_address(self, obj):
        return obj.user.address
    
    def get_date_of_birth(self, obj):
        return obj.user.date_of_birth
    
    def get_profile_picture(self, obj):
        return obj.user.profile_picture.url if obj.user.profile_picture else None
    
    def get_enrollment_count(self, obj):
        return obj.enrollments.count()
    
    def get_certificate_count(self, obj):
        return obj.certificates.count()


class EnrollmentSerializer(serializers.ModelSerializer):
    """Enrollment serializer"""
    student_name = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_name', 'course', 'course_title', 'status', 
            'enrollment_date', 'start_date', 'expected_completion_date', 
            'actual_completion_date', 'tuition_paid', 'notes', 'progress_percentage'
        ]
        read_only_fields = ['id', 'enrollment_date']
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    
    def get_course_title(self, obj):
        return obj.course.title
    
    def get_progress_percentage(self, obj):
        # Calculate progress based on completed modules/assessments
        total_modules = obj.course.modules.count()
        if total_modules == 0:
            return 0
        
        # This would need to be calculated based on actual progress tracking
        # For now, return a placeholder
        return 0


class AttendanceSerializer(serializers.ModelSerializer):
    """Attendance serializer"""
    student_name = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    recorded_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'enrollment', 'student_name', 'course_title', 'date', 
            'hours_attended', 'is_present', 'notes', 'recorded_by', 'recorded_by_name'
        ]
        read_only_fields = ['id']
    
    def get_student_name(self, obj):
        return obj.enrollment.student.user.get_full_name()
    
    def get_course_title(self, obj):
        return obj.enrollment.course.title
    
    def get_recorded_by_name(self, obj):
        return obj.recorded_by.get_full_name()


class AssessmentResultSerializer(serializers.ModelSerializer):
    """Assessment result serializer"""
    student_name = serializers.SerializerMethodField()
    assessment_title = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    graded_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AssessmentResult
        fields = [
            'id', 'enrollment', 'student_name', 'assessment', 'assessment_title', 
            'course_title', 'score', 'max_score', 'passed', 'attempt_number', 
            'completed_date', 'feedback', 'graded_by', 'graded_by_name'
        ]
        read_only_fields = ['id', 'completed_date']
    
    def get_student_name(self, obj):
        return obj.enrollment.student.user.get_full_name()
    
    def get_assessment_title(self, obj):
        return obj.assessment.title
    
    def get_course_title(self, obj):
        return obj.enrollment.course.title
    
    def get_graded_by_name(self, obj):
        return obj.graded_by.get_full_name()


class ProgressReportSerializer(serializers.ModelSerializer):
    """Progress report serializer"""
    student_name = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ProgressReport
        fields = [
            'id', 'enrollment', 'student_name', 'course_title', 'report_date', 
            'overall_progress', 'attendance_rate', 'average_score', 'strengths', 
            'areas_for_improvement', 'recommendations', 'created_by', 'created_by_name'
        ]
        read_only_fields = ['id']
    
    def get_student_name(self, obj):
        return obj.enrollment.student.user.get_full_name()
    
    def get_course_title(self, obj):
        return obj.enrollment.course.title
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name()


class PlacementSerializer(serializers.ModelSerializer):
    """Placement serializer"""
    student_name = serializers.SerializerMethodField()
    employer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Placement
        fields = [
            'id', 'student', 'student_name', 'employer', 'employer_name', 
            'job_title', 'start_date', 'end_date', 'salary', 'status', 
            'placement_fee', 'contract_document', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    
    def get_employer_name(self, obj):
        return obj.employer.company_name
