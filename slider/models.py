from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
import os
import uuid

def get_random_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('slider', filename)

# Create your models here.

class Slider(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    image = models.ImageField(upload_to=get_random_file_path, verbose_name="Image")
    description = models.TextField(verbose_name="Description Text", null=True, blank=True)
    link = models.URLField(max_length=1000, verbose_name="Link", null=True, blank=True)
    link_text = models.CharField(max_length=255, verbose_name="Link Text", null=True, blank=True)
    youtube_link = models.URLField(max_length=2000, verbose_name="Youtube Link", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.pk and Slider.objects.count() >= 3:
            raise ValidationError("Maximum number of sliders is 3")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"
        ordering = ['-created_at']

@receiver(pre_save, sender=Slider)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            old_instance = Slider.objects.get(pk=instance.pk)
            if old_instance.image and old_instance.image != instance.image:
                if os.path.isfile(old_instance.image.path):
                    os.remove(old_instance.image.path)
        except Slider.DoesNotExist:
            pass

@receiver(pre_delete, sender=Slider)
def delete_image_on_delete(sender, instance, *args, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class SliderSettings(models.Model):
    slider_text = models.TextField(verbose_name="Slider Text", null=True, blank=True)
    blue_background = models.BooleanField(default=False)

    def __str__(self):
        return "Slider Settings"
