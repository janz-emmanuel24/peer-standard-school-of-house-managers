from django.shortcuts import render
from courses.models import Course, CourseCategory


def home_view(request):
    """Home page view with course data"""
    # Get active courses grouped by category
    categories_with_courses = []
    
    # Get all active categories
    categories = CourseCategory.objects.filter(is_active=True).order_by('name')
    
    for category in categories:
        # Get active courses for this category
        courses = Course.objects.filter(
            category=category,
            status='active'
        ).order_by('title')[:3]  # Limit to 3 courses per category for display
        
        if courses.exists():
            categories_with_courses.append({
                'category': category,
                'courses': courses
            })
    
    context = {
        'categories_with_courses': categories_with_courses,
        'total_courses': Course.objects.filter(status='active').count(),
        'total_categories': CourseCategory.objects.filter(is_active=True).count(),
    }
    
    return render(request, 'home.html', context)
