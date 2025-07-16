import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='clean_html')
def clean_html(value):
    """
    Tehlikeli HTML etiketlerini kaldırır, güvenli olanları korur
    """
    if not value:
        return value
    
    # Kaldırılacak tehlikeli etiketler
    dangerous_tags = [
        'html', 'head', 'body', 'style', 'script'
    ]
    
    # Tehlikeli etiketleri kaldır (açılış ve kapanış)
    for tag in dangerous_tags:
        # Açılış etiketleri (attributes ile birlikte)
        pattern = r'<\s*' + tag + r'[^>]*?>'
        value = re.sub(pattern, '', value, flags=re.IGNORECASE)
        
        # Kapanış etiketleri
        pattern = r'<\s*/\s*' + tag + r'\s*>'
        value = re.sub(pattern, '', value, flags=re.IGNORECASE)
    
    # Boş satırları temizle
    value = re.sub(r'\n\s*\n', '\n', value)
    value = value.strip()
    
    return mark_safe(value) 