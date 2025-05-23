from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from solo.admin import SingletonModelAdmin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        ('SEO Information', {
            'fields': ('title', 'description', 'keywords', 'footer_description'),
            'description': 'Optimized site information for search engines'
        }),
        ('Site Images', {
            'fields': ('logo', 'favicon', 'footer_logo'),
            'description': 'Required images and icons for the site'
        }),
        ('Social Media', {
            'fields': ('facebook', 'instagram', 'twitter', 'linkedin', 'youtube', 'telegram', 'tiktok'),
            'description': 'Social media links'
        }),
    )

    def has_add_permission(self, request):
        if not SiteSettings.objects.exists():
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False
