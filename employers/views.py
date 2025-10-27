from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employer, JobPosting, JobApplication


@login_required
def employer_list(request):
    """List all employers"""
    employers = Employer.objects.filter(is_active=True)
    return render(request, 'employers/list.html', {'employers': employers})


@login_required
def employer_detail(request, employer_id):
    """Employer detail view"""
    employer = get_object_or_404(Employer, id=employer_id)
    job_postings = employer.job_postings.filter(status='active')
    return render(request, 'employers/detail.html', {
        'employer': employer,
        'job_postings': job_postings
    })


@login_required
def my_jobs(request):
    """Employer's job postings"""
    if not hasattr(request.user, 'employer_profile'):
        messages.error(request, 'Employer profile not found.')
        return redirect('dashboard:home')
    
    employer = request.user.employer_profile
    job_postings = employer.job_postings.all()
    return render(request, 'employers/my_jobs.html', {
        'employer': employer,
        'job_postings': job_postings
    })


@login_required
def post_job(request):
    """Post a new job"""
    if not hasattr(request.user, 'employer_profile'):
        messages.error(request, 'Employer profile not found.')
        return redirect('dashboard:home')
    
    employer = request.user.employer_profile
    
    if request.method == 'POST':
        # Create job posting logic here
        messages.success(request, 'Job posted successfully!')
        return redirect('employers:my_jobs')
    
    return render(request, 'employers/post_job.html', {'employer': employer})


@login_required
def job_list(request):
    """List all job postings"""
    jobs = JobPosting.objects.filter(status='active').select_related('employer')
    return render(request, 'employers/job_list.html', {'jobs': jobs})


@login_required
def job_detail(request, job_id):
    """Job posting detail"""
    job = get_object_or_404(JobPosting, id=job_id)
    applications = job.applications.all()
    
    # Check if user can apply
    can_apply = False
    if hasattr(request.user, 'student_profile'):
        can_apply = not job.applications.filter(
            student=request.user.student_profile
        ).exists()
    
    return render(request, 'employers/job_detail.html', {
        'job': job,
        'applications': applications,
        'can_apply': can_apply
    })


@login_required
def job_edit(request, job_id):
    """Edit job posting"""
    job = get_object_or_404(JobPosting, id=job_id)
    
    # Check permissions
    if not hasattr(request.user, 'employer_profile') or job.employer != request.user.employer_profile:
        if request.user.user_type != 'admin':
            messages.error(request, 'You do not have permission to edit this job.')
            return redirect('employers:job_detail', job_id=job_id)
    
    if request.method == 'POST':
        # Update job logic here
        messages.success(request, 'Job updated successfully!')
        return redirect('employers:job_detail', job_id=job_id)
    
    return render(request, 'employers/job_edit.html', {'job': job})