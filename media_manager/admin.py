from django.contrib import admin
from django.utils.html import format_html
from .models import Image, Video
from django.core.exceptions import ValidationError

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_image', 'display_thumbnail', 'created_at')
    list_display_links = ('title', 'display_image')
    readonly_fields = ('display_image_large', 'display_thumbnail_large', 'created_at', 'updated_at', 'thumbnail')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Image Information', {
            'fields': ('title', ('image', 'display_image_large'), ('display_thumbnail_large',))
        }),
    )

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image Preview'

    def display_thumbnail(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.thumbnail.url)
        return "No Thumbnail"
    display_thumbnail.short_description = 'Thumbnail Preview'

    def display_image_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="400" style="max-height: 400px; object-fit: contain;" />', obj.image.url)
        return "No Image"
    display_image_large.short_description = 'Image Preview (Large)'

    def display_thumbnail_large(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="200" style="max-height: 200px; object-fit: contain;" />', obj.thumbnail.url)
        return "No Thumbnail"
    display_thumbnail_large.short_description = 'Thumbnail Preview (Large)'

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_video', 'created_at')
    list_display_links = ('title',)
    readonly_fields = ('display_video_large', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Video Information', {
            'fields': ('title', ('video', 'display_video_large'), 'cover_image')
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'video':
            field.help_text = 'Maximum upload size: 100MB'
        return field

    def clean_video(self, video):
        if video:
            if video.size > 104857600:  # 100MB in bytes (100 * 1024 * 1024)
                raise ValidationError(format_html('<span style="color: red;">Video size cannot be greater than 100MB.</span>'))
        return video

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        old_clean = form.base_fields['video'].clean
        def clean_with_size(value, field=form.base_fields['video']):
            value = old_clean(value)
            return self.clean_video(value)
        form.base_fields['video'].clean = clean_with_size
        return form
    
    def display_video(self, obj):
        if obj.video:
            return format_html('<video width="100" height="60" controls><source src="{}" type="video/mp4"></video>', obj.video.url)
        return "No Video"
    display_video.short_description = 'Video Preview'

    def display_video_large(self, obj):
        if obj.video:
            return format_html('<video width="400" height="240" controls><source src="{}" type="video/mp4"></video>', obj.video.url)
        return "No Video"
    display_video_large.short_description = 'Video Preview (Large)'
