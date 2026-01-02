"""
Context processors for SEO and site-wide data
"""
from django.conf import settings


def seo(request):
    """
    Provides SEO metadata for templates
    """
    # Get the current URL path
    current_path = request.path
    
    # Default SEO values
    seo_data = {
        'site_name': 'Peer Standard Professional Workers',
        'site_description': 'Professional training and services for domestic workers. We provide comprehensive training, recruitment, and management services for workers, house owners, and organizations.',
        'site_keywords': 'maids, house helpers, domestic workers, professional training, worker recruitment, home care services, cleaning services, elderly care, Uganda, professional workers, house managers, nannies, caregivers, home assistants, domestic help, housekeeping, maid training, house helper training, professional maids, trained domestic workers, certified house helpers, Uganda maids, Kampala domestic workers, home care training, worker certification',
        'site_url': request.build_absolute_uri('/'),
        'site_image': request.build_absolute_uri(settings.STATIC_URL + 'images/logo_png_format.png'),
        'site_author': 'Peer Standard Professional Workers',
        'site_language': 'en',
        'canonical_url': request.build_absolute_uri(current_path),
    }
    
    # Page-specific SEO overrides
    page_seo = {
        '/': {
            'title': 'Peer Standard Professional Workers - Professional Training & Services',
            'description': 'Leading provider of professional training, recruitment, and management services for domestic workers in Uganda. Building professional excellence in home care.',
            'keywords': 'maids, house helpers, domestic workers training, professional cleaning services, elderly care, worker recruitment, Uganda, maid training, house helper training, professional maids, trained domestic workers, certified house helpers, Kampala maids, home care services',
        },
        '/about/': {
            'title': 'About Us - Peer Standard Professional Workers',
            'description': 'Learn about Peer Standard Professional Workers, our mission, values, and commitment to professional excellence in domestic services training and management.',
            'keywords': 'about us, professional training company, domestic services, Uganda, maids training, house helpers training, professional maids, certified domestic workers',
        },
        '/services/': {
            'title': 'Our Services - Professional Training & Management',
            'description': 'Comprehensive services including workers training, recruitment, management, professional cleaning, and elderly care services.',
            'keywords': 'maids training, house helpers training, workers training, recruitment services, worker management, professional cleaning, elderly care, maid recruitment, house helper recruitment, professional maids, trained domestic workers, nanny services, caregiver training',
        },
        '/clients/': {
            'title': 'Our Clients - Who We Serve',
            'description': 'We serve workers, house owners, patients, organizations, companies, and building owners with professional domestic services.',
            'keywords': 'clients, house owners, workers, organizations, companies',
        },
        '/programs/': {
            'title': 'Training Programs - Professional Development',
            'description': 'Comprehensive training programs designed to develop professional skills for domestic workers.',
            'keywords': 'maid training programs, house helper training, professional development, skills training, domestic worker certification, housekeeping training, nanny training, caregiver certification',
        },
        '/admissions/': {
            'title': 'Admissions - Join Our Training Programs',
            'description': 'Apply to join our professional training programs and start your journey to professional excellence.',
            'keywords': 'admissions, apply, training programs, enrollment, maid training enrollment, house helper training application, domestic worker courses, professional certification',
        },
        '/blog/': {
            'title': 'Blog - Latest News & Insights',
            'description': 'Stay updated with the latest news, insights, and tips from Peer Standard Professional Workers.',
            'keywords': 'blog, news, insights, tips, updates',
        },
        '/contact/': {
            'title': 'Contact Us - Get in Touch',
            'description': 'Contact Peer Standard Professional Workers for inquiries about our services, training programs, or partnerships.',
            'keywords': 'contact, get in touch, inquiries, support',
        },
    }
    
    # Update with page-specific data if available
    if current_path in page_seo:
        seo_data.update(page_seo[current_path])
    else:
        # Default title if not overridden
        seo_data['title'] = seo_data.get('title', 'Peer Standard Professional Workers')
    
    return {'seo': seo_data}


