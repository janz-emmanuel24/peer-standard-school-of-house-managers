"""
Sitemap configuration for SEO
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """
    Sitemap for static pages
    """
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return [
            'home',
            'about',
            'programs',
            'admissions',
            'contact',
            'services:index',
            'clients:index',
            'blog:index',
        ]

    def location(self, item):
        return reverse(item)


class ServicesSitemap(Sitemap):
    """
    Sitemap for services pages
    """
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return [
            'services:workers_training',
            'services:recruitment',
            'services:workers_management',
            'services:professional_cleaning',
            'services:elderly_care',
        ]

    def location(self, item):
        return reverse(item)


class ClientsSitemap(Sitemap):
    """
    Sitemap for clients pages
    """
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return [
            'clients:workers',
            'clients:house_owners',
            'clients:patients',
            'clients:organisations',
            'clients:companies',
            'clients:building_owners',
        ]

    def location(self, item):
        return reverse(item)


