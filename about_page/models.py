from django.db import models
from ckeditor.fields import RichTextField


class AboutPage(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = RichTextField(verbose_name="Description")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"