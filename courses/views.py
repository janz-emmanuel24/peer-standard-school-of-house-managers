from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, CourseCategory, Instructor


def course_list(request):
    """List all courses - accessible to everyone"""
    courses = Course.objects.filter(status='active').select_related('category')
    categories = CourseCategory.objects.filter(is_active=True)
    return render(request, 'courses/list.html', {
        'courses': courses,
        'categories': categories
    })


def course_detail(request, course_id):
    """Course detail view - accessible to everyone"""
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.all()
    assessments = course.assessments.all()
    instructors = course.courseinstructor_set.all()
    
    # Check if user is enrolled (only for authenticated users)
    is_enrolled = False
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        is_enrolled = course.enrollments.filter(
            student=request.user.student_profile
        ).exists()
    
    return render(request, 'courses/detail.html', {
        'course': course,
        'modules': modules,
        'assessments': assessments,
        'instructors': instructors,
        'is_enrolled': is_enrolled
    })


@login_required
def course_create(request):
    """Create new course (admin/instructor only)"""
    if request.user.user_type not in ['admin', 'instructor']:
        messages.error(request, 'You do not have permission to create courses.')
        return redirect('courses:list')
    
    if request.method == 'POST':
        # Create course logic here
        messages.success(request, 'Course created successfully!')
        return redirect('courses:list')
    
    categories = CourseCategory.objects.filter(is_active=True)
    return render(request, 'courses/create.html', {'categories': categories})


@login_required
def course_edit(request, course_id):
    """Edit course (admin/instructor only)"""
    if request.user.user_type not in ['admin', 'instructor']:
        messages.error(request, 'You do not have permission to edit courses.')
        return redirect('courses:list')
    
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        # Update course logic here
        messages.success(request, 'Course updated successfully!')
        return redirect('courses:detail', course_id=course_id)
    
    categories = CourseCategory.objects.filter(is_active=True)
    return render(request, 'courses/edit.html', {
        'course': course,
        'categories': categories
    })


@login_required
def course_enroll(request, course_id):
    """Enroll in course"""
    course = get_object_or_404(Course, id=course_id)
    
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Student profile not found.')
        return redirect('courses:detail', course_id=course_id)
    
    return redirect('students:enroll', course_id=course_id)


def category_list(request):
    """List course categories - accessible to everyone"""
    categories = CourseCategory.objects.filter(is_active=True)
    return render(request, 'courses/categories.html', {'categories': categories})