from django.db import models
import uuid
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('media_manager', instance.__class__.__name__.lower(), filename)

class Image(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    image = models.ImageField(upload_to=get_file_path, verbose_name="Image")
    thumbnail = models.ImageField(upload_to='thumbs/', verbose_name="Thumbnail", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ['-created_at']
        

class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    cover_image = models.ImageField(upload_to='videos/covers/', verbose_name="Cover Image", null=True, blank=True)
    video = models.FileField(upload_to=get_file_path, verbose_name="Video")
    thumbnail = models.ImageField(upload_to='thumbs/', verbose_name="Thumbnail", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"
        ordering = ['-created_at']
