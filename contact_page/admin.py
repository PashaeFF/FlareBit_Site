from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


@admin.register(EmailInbox)
class EmailInboxAdmin(admin.ModelAdmin):
    list_display = ('email_display', 'name', 'service_type', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at', 'service_type')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
    
    def email_display(self, obj):
        if not obj.is_read:
            return mark_safe(f'<b style="font-weight: 800;">{obj.email}</b>')
        else:
            return mark_safe(f'<span style="font-weight: 400;">{obj.email}</span>')
    email_display.short_description = 'Email'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and not obj.is_read:
            obj.is_read = True
            obj.save()
        return super().change_view(request, object_id, form_url, extra_context)

    def view_on_site(self, obj):
        if obj and not obj.is_read:
            obj.is_read = True
            obj.save()
        return None

@admin.register(WhatsappNumber)
class WhatsappNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_active', 'general_number')
    list_filter = ('is_active', 'general_number')

@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_active')
    list_filter = ('is_active',)

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active')
    list_filter = ('is_active',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'location_link', 'is_active')
    list_filter = ('is_active',)

@admin.register(MapEmbed)
class MapEmbedAdmin(admin.ModelAdmin):
    list_display = ('short_embed_code', 'is_active')
    list_filter = ('is_active',)
    
    def short_embed_code(self, obj):
        return obj.embed_code[:50] + "..." if len(obj.embed_code) > 50 else obj.embed_code
    short_embed_code.short_description = "Google Map Embed Code"

    def has_add_permission(self, request):
        return not MapEmbed.objects.exists()

@admin.register(ContactEmail)
class ContactEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active')
    list_filter = ('is_active',)
