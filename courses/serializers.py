from rest_framework import serializers
from .models import CourseCategory, Course, CourseModule, Instructor, CourseInstructor, Assessment


class CourseCategorySerializer(serializers.ModelSerializer):
    """Course category serializer"""
    course_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'description', 'is_active', 'course_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_course_count(self, obj):
        return obj.courses.filter(status='active').count()


class CourseModuleSerializer(serializers.ModelSerializer):
    """Course module serializer"""
    class Meta:
        model = CourseModule
        fields = [
            'id', 'title', 'description', 'order', 'duration_hours', 
            'content', 'is_required', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class InstructorSerializer(serializers.ModelSerializer):
    """Instructor serializer"""
    full_name = serializers.SerializerMethodField()
    course_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Instructor
        fields = [
            'id', 'user', 'full_name', 'employee_id', 'specialization', 
            'years_experience', 'hourly_rate', 'is_active', 'bio', 
            'certifications', 'course_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    
    def get_course_count(self, obj):
        return obj.courseinstructor_set.filter(course__status='active').count()


class CourseInstructorSerializer(serializers.ModelSerializer):
    """Course instructor serializer"""
    instructor_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CourseInstructor
        fields = ['id', 'course', 'instructor', 'instructor_name', 'is_primary', 'assigned_date']
        read_only_fields = ['id', 'assigned_date']
    
    def get_instructor_name(self, obj):
        return obj.instructor.user.get_full_name()


class AssessmentSerializer(serializers.ModelSerializer):
    """Assessment serializer"""
    class Meta:
        model = Assessment
        fields = [
            'id', 'course', 'title', 'assessment_type', 'description', 
            'max_score', 'passing_score', 'duration_minutes', 'instructions', 
            'is_required', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    """Course serializer"""
    category_name = serializers.SerializerMethodField()
    instructor_count = serializers.SerializerMethodField()
    enrollment_count = serializers.SerializerMethodField()
    modules = CourseModuleSerializer(many=True, read_only=True)
    assessments = AssessmentSerializer(many=True, read_only=True)
    instructors = CourseInstructorSerializer(source='courseinstructor_set', many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'category', 'category_name', 
            'difficulty_level', 'duration_weeks', 'total_hours', 'max_students', 
            'tuition_fee', 'status', 'prerequisites', 'learning_outcomes', 
            'course_materials', 'created_by', 'instructor_count', 'enrollment_count',
            'modules', 'assessments', 'instructors', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_instructor_count(self, obj):
        return obj.courseinstructor_set.count()
    
    def get_enrollment_count(self, obj):
        return obj.enrollments.filter(status='enrolled').count()


class CourseListSerializer(serializers.ModelSerializer):
    """Simplified course serializer for list views"""
    category_name = serializers.SerializerMethodField()
    enrollment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'category_name', 'difficulty_level', 
            'duration_weeks', 'total_hours', 'tuition_fee', 'status', 
            'enrollment_count', 'created_at'
        ]
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_enrollment_count(self, obj):
        return obj.enrollments.filter(status='enrolled').count()
