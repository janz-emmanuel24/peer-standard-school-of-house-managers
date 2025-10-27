from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Certificate, CertificateTemplate, CertificateVerification


@login_required
def certificate_list(request):
    """List certificates"""
    if hasattr(request.user, 'student_profile'):
        certificates = request.user.student_profile.certificates.all()
    else:
        certificates = Certificate.objects.all()
    
    return render(request, 'certifications/list.html', {'certificates': certificates})


@login_required
def certificate_detail(request, certificate_id):
    """Certificate detail view"""
    certificate = get_object_or_404(Certificate, id=certificate_id)
    
    # Check permissions
    if hasattr(request.user, 'student_profile'):
        if certificate.student != request.user.student_profile:
            messages.error(request, 'You do not have permission to view this certificate.')
            return redirect('certifications:list')
    
    verifications = certificate.verifications.all()
    return render(request, 'certifications/detail.html', {
        'certificate': certificate,
        'verifications': verifications
    })


@login_required
def verify_certificate(request):
    """Verify certificate by code"""
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        try:
            certificate = Certificate.objects.get(verification_code=verification_code)
            return render(request, 'certifications/verify_result.html', {
                'certificate': certificate,
                'is_valid': True
            })
        except Certificate.DoesNotExist:
            return render(request, 'certifications/verify_result.html', {
                'is_valid': False,
                'error': 'Invalid verification code'
            })
    
    return render(request, 'certifications/verify.html')


@login_required
def certificate_download(request, certificate_id):
    """Download certificate"""
    certificate = get_object_or_404(Certificate, id=certificate_id)
    
    # Check permissions
    if hasattr(request.user, 'student_profile'):
        if certificate.student != request.user.student_profile:
            messages.error(request, 'You do not have permission to download this certificate.')
            return redirect('certifications:list')
    
    if certificate.certificate_file:
        response = HttpResponse(certificate.certificate_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{certificate.certificate_number}.pdf"'
        return response
    else:
        messages.error(request, 'Certificate file not available.')
        return redirect('certifications:detail', certificate_id=certificate_id)


@login_required
def template_list(request):
    """List certificate templates (admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to view templates.')
        return redirect('dashboard:home')
    
    templates = CertificateTemplate.objects.filter(is_active=True)
    return render(request, 'certifications/templates.html', {'templates': templates})


@login_required
def template_create(request):
    """Create certificate template (admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to create templates.')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        # Create template logic here
        messages.success(request, 'Template created successfully!')
        return redirect('certifications:templates')
    
    return render(request, 'certifications/template_create.html')