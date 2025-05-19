from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Image, Video
from PIL import Image as PILImage
import os
import uuid

def create_thumbnail(image_path, size=(300, 300)):
    img = PILImage.open(image_path)
    img.thumbnail(size)
    
    filename = f"{uuid.uuid4()}.{img.format.lower()}"
    thumbnail_path = os.path.join('media', 'thumbs', filename)
    
    os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
    
    img.save(thumbnail_path)
    return os.path.join('thumbs', filename)

@receiver(post_save, sender=Image)
def generate_image_thumbnail(sender, instance, created, **kwargs):
    if created or not instance.thumbnail:
        if instance.image:
            image_path = instance.image.path
            thumbnail_path = create_thumbnail(image_path)
            instance.thumbnail.name = thumbnail_path
            instance.save(update_fields=['thumbnail'])

@receiver(post_save, sender=Video)
def generate_video_thumbnail(sender, instance, created, **kwargs):
    # Video thumbnail oluşturma işlemi buraya eklenebilir
    # FFmpeg gibi bir kütüphane kullanılarak video'dan thumbnail oluşturulabilir
    pass

@receiver(pre_delete, sender=Image)
def delete_image_files(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
    
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)

@receiver(pre_delete, sender=Video)
def delete_video_files(sender, instance, **kwargs):
    if instance.video:
        if os.path.isfile(instance.video.path):
            os.remove(instance.video.path)
    
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path) 