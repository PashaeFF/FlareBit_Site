from django.db import models
from solo.models import SingletonModel
import uuid
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('site_settings', filename)

# Create your models here.
class SiteSettings(SingletonModel):
    title = models.CharField(
        max_length=255,
        verbose_name="Site title",
        help_text="Site title and the name that will appear in the browser tab"
    )
    description = models.TextField(
        verbose_name="Site description",
        help_text="Site description that will appear in search engines like Google",
        null=True,
        blank=True
    )

    keywords = models.TextField(
        verbose_name="Keywords",
        help_text="Keywords for search engines (separated by commas)",
        null=True,
        blank=True
    )
    logo = models.ImageField(
        upload_to=get_file_path,
        null=True,
        blank=True,
        verbose_name="Site Logo",
        help_text="Site logo (recommended size: 200x50px)"
    )

    footer_logo = models.ImageField(
        upload_to=get_file_path,
        null=True,
        blank=True,
        verbose_name="Footer Logo",
        help_text="Footer logo (recommended size: 200x50px)"
    )
    favicon = models.ImageField(
        upload_to=get_file_path,
        null=True,
        blank=True,
        verbose_name="Favicon",
        help_text="Browser tab icon (recommended size: 32x32px)"
    )
    # cover_image = models.ImageField(
    #     upload_to=get_file_path,
    #     null=True,
    #     blank=True,
    #     verbose_name="Cover Image",
    #     help_text="Cover image for the homepage (recommended size: 1920x1080px)"
    # )

    footer_description = models.TextField(
        verbose_name="Footer Description",
        help_text="Footer description that will appear in the footer",
        null=True,
        blank=True
    )
  
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    tiktok = models.URLField(null=True, blank=True)
    
    
    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def delete_old_image(self, field_name):
        """Eski görseli sil"""
        try:
            # Mevcut nesneyi veritabanından al
            old_instance = SiteSettings.objects.get(pk=self.pk)
            old_file = getattr(old_instance, field_name)
            # Yeni dosya farklıysa ve eski dosya varsa
            if old_file and old_file != getattr(self, field_name):
                if os.path.isfile(old_file.path):
                    os.remove(old_file.path)
        except (SiteSettings.DoesNotExist, ValueError, OSError):
            pass

    def save(self, *args, **kwargs):
        # Eğer bu yeni bir kayıt değilse
        if self.pk:
            self.delete_old_image('logo')
            self.delete_old_image('favicon')
            self.delete_old_image('footer_logo')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Tüm görselleri sil
        for field in ['logo', 'favicon', 'footer_logo']:
            file = getattr(self, field)
            if file:
                if os.path.isfile(file.path):
                    os.remove(file.path)
        super().delete(*args, **kwargs)

    
