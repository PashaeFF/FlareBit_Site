from django.contrib import admin
from html import escape
from django.utils.safestring import mark_safe
from .models import AboutPage

class AboutPageAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title'].help_text = escape('Write any text between these tags to make it special: <span class="text-theme">') + mark_safe('<span style="color:red">YOUR TEXT</span>') + escape('</span>')
        return form

admin.site.register(AboutPage, AboutPageAdmin)