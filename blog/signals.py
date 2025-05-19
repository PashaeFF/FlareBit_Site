import os
from PIL import Image
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.files.base import ContentFile
from io import BytesIO
from .models import Blog

@receiver(post_save, sender=Blog)
def create_thumbnail(sender, instance, created, **kwargs):
    if instance.image:
        # Eğer thumbnail zaten varsa ve resim değişmediyse işlem yapma
        if instance.image_thumbnail and instance.image_thumbnail.name:
            if 'thumb_' + os.path.basename(instance.image.name) == os.path.basename(instance.image_thumbnail.name):
                return

        # Orijinal resmi aç
        img = Image.open(instance.image)
        
        # RGBA formatındaysa RGB'ye çevir
        if img.mode in ('RGBA', 'LA'):
            img = img.convert('RGB')
        
        # Thumbnail boyutu
        THUMBNAIL_SIZE = (300, 300)
        
        # En-boy oranını koruyarak thumbnail oluştur
        img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
        
        # BytesIO kullanarak thumbnail'i kaydet
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)
        
        # Orijinal resmin ismini al ve thumbnail için düzenle
        original_name = os.path.basename(instance.image.name)
        thumbnail_name = f'thumb_{original_name}'
        
        # Eski thumbnail varsa sil
        if instance.image_thumbnail:
            instance.image_thumbnail.delete(save=False)
        
        # Yeni thumbnail'i kaydet
        instance.image_thumbnail.save(
            thumbnail_name,
            ContentFile(thumb_io.getvalue()),
            save=False
        )
        instance.save()

@receiver(pre_delete, sender=Blog)
def delete_files(sender, instance, **kwargs):
    # Blog silindiğinde resim ve thumbnail'i de sil
    if instance.image:
        instance.image.delete(False)
    if instance.image_thumbnail:
        instance.image_thumbnail.delete(False) 