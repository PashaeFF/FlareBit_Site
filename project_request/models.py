from django.db import models
from services.models import Service

class HowDidYouHearAboutUs(models.Model):
    class Meta:
        verbose_name = "How Did You Hear About Us"
        verbose_name_plural = "How Did You Hear About Us"
        
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
class ProjectRequest(models.Model):
    class Meta:
        verbose_name = "Project Request"
        verbose_name_plural = "Project Requests"

    description = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    request_date = models.DateField(null=True, blank=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    how_did_you_hear_about_us = models.ForeignKey(HowDidYouHearAboutUs, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
    

class ProjectFiles(models.Model):
    class Meta:
        verbose_name = "Project File"
        verbose_name_plural = "Project Files"
        
    file = models.FileField(upload_to='project_files/')
    project_request = models.ForeignKey(ProjectRequest, on_delete=models.CASCADE, related_name='project_files')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name