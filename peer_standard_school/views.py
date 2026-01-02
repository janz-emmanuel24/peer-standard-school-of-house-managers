from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
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


@require_http_methods(["GET"])
def robots_txt(request):
    """Serve robots.txt file"""
    robots_content = """# robots.txt for Peer Standard Professional Workers

User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /dashboard/
Disallow: /accounts/
Disallow: /students/
Disallow: /courses/
Disallow: /employers/
Disallow: /certifications/
Disallow: /financials/

# Sitemap
Sitemap: {protocol}://{domain}/sitemap.xml

# Crawl-delay (optional, adjust as needed)
Crawl-delay: 1
""".format(
        protocol=request.scheme,
        domain=request.get_host()
    )
    return HttpResponse(robots_content, content_type='text/plain')
