from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField


class EmailInbox(models.Model):
    class Meta:
        verbose_name = "Email Inbox"
        verbose_name_plural = "Email Inbox"

    name = models.CharField(max_length=255)
    email = models.EmailField()
    service_type = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
# Create your models here.
class PhoneNumber(models.Model):
    number = PhoneNumberField(
        unique=True,
        error_messages={
            'invalid': 'Please enter a valid phone number (e.g. +994501234567)',
            'unique': 'This phone number is already registered'
        }
    )
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.number:
            if not self.number.is_valid():
                raise ValidationError({
                    'number': 'Invalid phone number format'
                })
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.number:
            return self.number.as_international
        return str(self.number)

    class Meta:
        verbose_name = 'Phone Number'
        verbose_name_plural = 'Phone Numbers'


class WhatsappNumber(models.Model):
    class Meta:
        verbose_name = "Whatsapp Number"
        verbose_name_plural = "Whatsapp Numbers"

    number = PhoneNumberField(
        unique=True,
        error_messages={
            'invalid': 'Please enter a valid phone number (e.g. +994501234567)',
            'unique': 'This phone number is already registered'
        }
    )
    is_active = models.BooleanField(default=True)
    general_number = models.BooleanField(default=False)

    def clean(self):
        if self.number:
            if not self.number.is_valid():
                raise ValidationError({
                    'number': 'Invalid phone number format'
                })

class Email(models.Model):
    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"

    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    
class Address(models.Model):
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    address = models.TextField()
    location_link = models.URLField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.address
        
class ContactEmail(models.Model):
    class Meta:
        verbose_name = "Contact Email"
        verbose_name_plural = "Contact Emails"

    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class MapEmbed(models.Model):
    class Meta:
        verbose_name = "Google Map Embed"
        verbose_name_plural = "Google Map Embeds"

    embed_code = models.TextField()
    is_active = models.BooleanField(default=True)

    def clean(self):
        if MapEmbed.objects.exists() and not self.pk:
            raise ValidationError("Just one map embed is allowed")

    def __str__(self):
        return self.embed_code[:50] + "..." if len(self.embed_code) > 50 else self.embed_code
