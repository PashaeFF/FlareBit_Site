from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import uuid
import os
from django.utils.text import slugify

def generate_unique_filename(instance, filename):
    # Dosya uzantısını al
    ext = filename.split('.')[-1]
    # UUID ile benzersiz isim oluştur
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    # Dosya yolunu döndür
    return os.path.join('blog_images', unique_filename)

# Create your models here.

class BlogCategory(models.Model):
    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

            original_slug = self.slug
            counter = 1
            while BlogCategory.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

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
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, null=True, blank=True)
    youtube_link = models.URLField(max_length=2000, null=True, blank=True)
    video_link = models.URLField(max_length=2000, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

            original_slug = self.slug
            counter = 1
            while Blog.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title