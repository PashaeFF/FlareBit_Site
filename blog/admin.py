from django.contrib import admin
from .models import Blog, BlogCategory

# Register your models here.

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {}  # slug alanını boş bırakıyoruz çünkü otomatik oluşacak

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Eğer düzenleme ise
            return self.readonly_fields
        return self.readonly_fields + ('slug',)  # Yeni oluşturmada slug readonly

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'is_active', 'created_at', 'updated_at')
    list_filter = ('category', 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {}  # slug alanını boş bırakıyoruz çünkü otomatik oluşacak
    fields = ('title', 'category', 'description', 'image', 'link', 'link_text', 'youtube_embed_code', 'video_link', 'is_active')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Eğer düzenleme ise
            return self.readonly_fields
        return self.readonly_fields + ('slug',)  # Yeni oluşturmada slug readonly

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Category alanını zorunlu hale getir
        if 'category' in form.base_fields:
            form.base_fields['category'].required = True
        return form
