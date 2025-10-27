from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from accounts.models import User
from students.models import Student, Enrollment, Placement
from courses.models import Course
from employers.models import Employer, JobPosting
from financials.models import Payment, Payroll, Expense


@login_required
def dashboard_home(request):
    """Main dashboard view with KPIs and statistics"""
    user = request.user
    
    # Get current date and calculate date ranges
    today = timezone.now().date()
    this_month = today.replace(day=1)
    last_month = (this_month - timedelta(days=1)).replace(day=1)
    
    # Base statistics
    stats = {
        'total_students': Student.objects.filter(is_active=True).count(),
        'total_courses': Course.objects.filter(status='active').count(),
        'total_employers': Employer.objects.filter(is_active=True).count(),
        'total_placements': Placement.objects.filter(status='placed').count(),
    }
    
    # Monthly statistics
    monthly_stats = {
        'new_students': Student.objects.filter(enrollment_date__date__gte=this_month).count(),
        'new_enrollments': Enrollment.objects.filter(enrollment_date__date__gte=this_month).count(),
        'new_placements': Placement.objects.filter(created_at__date__gte=this_month).count(),
        'revenue': Payment.objects.filter(
            payment_date__date__gte=this_month,
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0,
    }
    
    # Recent activities
    recent_enrollments = Enrollment.objects.select_related(
        'student__user', 'course'
    ).order_by('-enrollment_date')[:5]
    
    recent_placements = Placement.objects.select_related(
        'student__user', 'employer'
    ).order_by('-created_at')[:5]
    
    recent_jobs = JobPosting.objects.select_related('employer').order_by('-created_at')[:5]
    
    # Course completion rates
    course_stats = []
    for course in Course.objects.filter(status='active')[:5]:
        total_enrollments = Enrollment.objects.filter(course=course).count()
        completed_enrollments = Enrollment.objects.filter(
            course=course, 
            status='completed'
        ).count()
        completion_rate = (completed_enrollments / total_enrollments * 100) if total_enrollments > 0 else 0
        
        course_stats.append({
            'course': course,
            'total_enrollments': total_enrollments,
            'completed_enrollments': completed_enrollments,
            'completion_rate': round(completion_rate, 1)
        })
    
    # Financial summary
    financial_summary = {
        'total_revenue': Payment.objects.filter(
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0,
        'monthly_revenue': monthly_stats['revenue'],
        'pending_payments': Payment.objects.filter(
            status='pending'
        ).aggregate(total=Sum('amount'))['total'] or 0,
        'total_expenses': Expense.objects.aggregate(total=Sum('amount'))['total'] or 0,
    }
    
    context = {
        'stats': stats,
        'monthly_stats': monthly_stats,
        'recent_enrollments': recent_enrollments,
        'recent_placements': recent_placements,
        'recent_jobs': recent_jobs,
        'course_stats': course_stats,
        'financial_summary': financial_summary,
        'user': user,
    }
    
    return render(request, 'dashboard/home.html', context)


@login_required
def reports_view(request):
    """Reports and analytics view"""
    # Generate various reports based on user permissions
    reports = []
    
    if request.user.user_type in ['admin', 'instructor']:
        # Student performance report
        student_performance = Student.objects.annotate(
            total_enrollments=Count('enrollments'),
            completed_courses=Count('enrollments', filter=models.Q(enrollments__status='completed'))
        ).order_by('-total_enrollments')[:10]
        
        reports.append({
            'title': 'Top Performing Students',
            'data': student_performance,
            'type': 'student_performance'
        })
        
        # Course popularity report
        course_popularity = Course.objects.annotate(
            enrollment_count=Count('enrollments')
        ).order_by('-enrollment_count')[:10]
        
        reports.append({
            'title': 'Most Popular Courses',
            'data': course_popularity,
            'type': 'course_popularity'
        })
    
    if request.user.user_type == 'admin':
        # Financial report
        monthly_revenue = []
        for i in range(12):
            month_start = today.replace(day=1) - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            revenue = Payment.objects.filter(
                payment_date__date__gte=month_start,
                payment_date__date__lt=month_end,
                status='completed'
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            monthly_revenue.append({
                'month': month_start.strftime('%b %Y'),
                'revenue': revenue
            })
        
        reports.append({
            'title': 'Monthly Revenue Trend',
            'data': monthly_revenue,
            'type': 'revenue_trend'
        })
    
    context = {
        'reports': reports,
        'user': request.user,
    }
    
    return render(request, 'dashboard/reports.html', context)