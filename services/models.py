from django.db import models
from ckeditor.fields import RichTextField


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
    youtube_link = models.URLField(max_length=1000, null=True, blank=True)
    ordering = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.title

