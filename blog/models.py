from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import uuid
import os

def generate_unique_filename(instance, filename):
    # Dosya uzantısını al
    ext = filename.split('.')[-1]
    # UUID ile benzersiz isim oluştur
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    # Dosya yolunu döndür
    return os.path.join('blog_images', unique_filename)

# Create your models here.

class Blog(models.Model):
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    title = models.CharField(max_length=255)
    description = RichTextUploadingField(
        verbose_name='Description',
        help_text='Blog description with rich text editor and image upload capability'
    )
    link = models.URLField(max_length=1000, null=True, blank=True)
    link_text = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(
        upload_to=generate_unique_filename,
        null=True,
        blank=True
    )
    image_thumbnail = models.ImageField(
        upload_to='blog_images/thumbnails/',
        null=True,
        blank=True,
        editable=False
    )
    youtube_link = models.URLField(max_length=2000, null=True, blank=True)
    video_link = models.URLField(max_length=2000, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title