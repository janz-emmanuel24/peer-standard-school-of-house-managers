from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Enrollment
from courses.models import Course


@login_required
def student_list(request):
    """List all students"""
    students = Student.objects.filter(is_active=True).select_related('user')
    return render(request, 'students/list.html', {'students': students})


@login_required
def student_detail(request, student_id):
    """Student detail view"""
    student = get_object_or_404(Student, id=student_id)
    enrollments = student.enrollments.all()
    return render(request, 'students/detail.html', {
        'student': student,
        'enrollments': enrollments
    })


@login_required
def my_courses(request):
    """Student's enrolled courses"""
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Student profile not found.')
        return redirect('dashboard:home')
    
    student = request.user.student_profile
    enrollments = student.enrollments.all()
    return render(request, 'students/my_courses.html', {
        'student': student,
        'enrollments': enrollments
    })


@login_required
def my_certificates(request):
    """Student's certificates"""
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Student profile not found.')
        return redirect('dashboard:home')
    
    student = request.user.student_profile
    certificates = student.certificates.all()
    return render(request, 'students/certificates.html', {
        'student': student,
        'certificates': certificates
    })


@login_required
def enrollment_list(request):
    """List all enrollments (admin/instructor view)"""
    enrollments = Enrollment.objects.select_related('student__user', 'course')
    return render(request, 'students/enrollments.html', {'enrollments': enrollments})


@login_required
def enroll_course(request, course_id):
    """Enroll in a course"""
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Student profile not found.')
        return redirect('dashboard:home')
    
    course = get_object_or_404(Course, id=course_id)
    student = request.user.student_profile
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=student, course=course).exists():
        messages.warning(request, 'You are already enrolled in this course.')
        return redirect('courses:detail', course_id=course_id)
    
    if request.method == 'POST':
        enrollment = Enrollment.objects.create(
            student=student,
            course=course,
            status='enrolled'
        )
        messages.success(request, f'Successfully enrolled in {course.title}!')
        return redirect('students:my_courses')
    
    return render(request, 'students/enroll_confirm.html', {'course': course})


@login_required
def student_edit(request, student_id):
    """Edit student profile"""
    student = get_object_or_404(Student, id=student_id)
    
    # Check permissions
    if request.user != student.user and request.user.user_type not in ['admin', 'instructor']:
        messages.error(request, 'You do not have permission to edit this profile.')
        return redirect('students:detail', student_id=student_id)
    
    if request.method == 'POST':
        # Update student fields
        student.gender = request.POST.get('gender')
        student.marital_status = request.POST.get('marital_status')
        student.emergency_contact_name = request.POST.get('emergency_contact_name')
        student.emergency_contact_phone = request.POST.get('emergency_contact_phone')
        student.emergency_contact_relationship = request.POST.get('emergency_contact_relationship')
        student.education_level = request.POST.get('education_level')
        student.previous_experience = request.POST.get('previous_experience')
        student.languages_spoken = request.POST.get('languages_spoken')
        student.special_skills = request.POST.get('special_skills')
        student.medical_conditions = request.POST.get('medical_conditions')
        student.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('students:detail', student_id=student_id)
    
    return render(request, 'students/edit.html', {'student': student})