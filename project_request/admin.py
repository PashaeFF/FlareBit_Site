from django.contrib import admin
from .models import HowDidYouHearAboutUs, ProjectRequest, ProjectFiles

@admin.register(HowDidYouHearAboutUs)
class HowDidYouHearAboutUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ('contact_name', 'email', 'organization', 'is_read', 'is_approved', 'is_rejected', 'is_pending', 'is_completed', 'created_at')
    list_filter = ('is_read', 'is_approved', 'is_rejected', 'is_pending', 'is_completed', 'request_date')
    search_fields = ('contact_name', 'email', 'organization', 'description')
    readonly_fields = ('created_at',)

@admin.register(ProjectFiles)
class ProjectFilesAdmin(admin.ModelAdmin):
    list_display = ('project_request', 'file', 'created_at')
    search_fields = ('project_request__contact_name', 'file')
    readonly_fields = ('created_at',)
