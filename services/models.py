from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class Service(models.Model):
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    title = models.CharField(max_length=255)
    description = RichTextField(
        config_name='default',
        verbose_name='Description',
        help_text='Service description with rich text editor'
    )
    icon = models.ImageField(upload_to='services/icons/')
    is_active = models.BooleanField(default=True)
    link = models.URLField(max_length=1000, null=True, blank=True)
    link_text = models.CharField(max_length=255, null=True, blank=True)
    video_link = models.URLField(max_length=1000, null=True, blank=True)
    youtube_embed_code = models.TextField(null=True, blank=True)
    ordering = models.PositiveIntegerField(default=0, blank=False, null=False)
    slug = models.SlugField(max_length=555, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

            original_slug = self.slug
            counter = 1
            while Service.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

