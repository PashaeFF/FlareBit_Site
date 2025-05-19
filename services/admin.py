from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'ordering')
    list_filter = ('is_active',)
    search_fields = ('title',)
