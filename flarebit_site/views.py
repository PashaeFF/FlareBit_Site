from django.shortcuts import render, redirect
from site_settings.models import SiteSettings
from slider.models import Slider, SliderSettings
from about_page.models import AboutPage
from blog.models import Blog, BlogCategory
from services.models import Service
from project_request.models import HowDidYouHearAboutUs
from contact_page.models import *
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import get_page_range, ALLOWED_MIME_TYPES, ALLOWED_EXTENSIONS
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from flarebit_site.serializers import ProjectRequestSerializer, ProjectFiles
import os
import re
from django.utils.safestring import mark_safe


def home(request):
    settings = SiteSettings.objects.first()
    phone_number = PhoneNumber.objects.filter(is_active=True).first()
    sliders = Slider.objects.all()
    slider_settings = SliderSettings.objects.first()
    whatsapp_number = WhatsappNumber.objects.filter(is_active=True, general_number=True).first()
    services = Service.objects.filter(is_active=True, ordering__gt=0).order_by('ordering')
    services_all = Service.objects.filter(is_active=True).order_by('ordering')
    how_did_you_hear_about_us = HowDidYouHearAboutUs.objects.all()
    
    context = {
        'title': settings.title if settings else 'Flarebit',
        'site_settings': settings if settings else None,
        'sliders': sliders if sliders else None,
        'slider_settings': slider_settings if slider_settings else None,
        'services': services if services else None, 
        'phone_number': phone_number.number if phone_number else None,
        'whatsapp_number': whatsapp_number.number if whatsapp_number else None,
        'services_all': services_all if services_all else None,
        'how_did_you_hear_about_us': how_did_you_hear_about_us if how_did_you_hear_about_us else None,
    }
    return render(request, 'home.html', context)


def about(request):
    settings = SiteSettings.objects.first()
    about_page = AboutPage.objects.all()
    whatsapp_number = WhatsappNumber.objects.filter(is_active=True, general_number=True).first()
    phone_number = PhoneNumber.objects.filter(is_active=True).first()
    context = {
        'title': f"{settings.title} - About Us" if settings else 'About Us',
        'site_settings': settings if settings else None,
        'page_name': 'About Us',
        'about_page': about_page if about_page else None,
        'whatsapp_number': whatsapp_number.number if whatsapp_number else None,
        'phone_number': phone_number.number if phone_number else None,
    }
    return render(request, 'about.html', context)

def services(request):
    settings = SiteSettings.objects.first()
    services_all = Service.objects.filter(is_active=True).order_by('ordering')
    whatsapp_number = WhatsappNumber.objects.filter(is_active=True, general_number=True).first()
    phone_number = PhoneNumber.objects.filter(is_active=True).first()
    how_did_you_hear_about_us = HowDidYouHearAboutUs.objects.all()
    context = {
        'title': f"{settings.title} - Services" if settings else 'Services',
        'site_settings': settings if settings else None,
        'services': services_all if services_all else None,
        'page_name': 'Services',
        'whatsapp_number': whatsapp_number.number if whatsapp_number else None,
        'phone_number': phone_number.number if phone_number else None,
        'how_did_you_hear_about_us': how_did_you_hear_about_us if how_did_you_hear_about_us else None,
        'services_all': services_all if services_all else None,
    }
    return render(request, 'services.html', context)

def service_details(request, slug):
    try:
        settings = SiteSettings.objects.first()
        service = Service.objects.get(slug=slug)
        services_all = Service.objects.filter(is_active=True).order_by('ordering')
        whatsapp_number = WhatsappNumber.objects.filter(is_active=True, general_number=True).first()
        phone_number = PhoneNumber.objects.filter(is_active=True).first()
        how_did_you_hear_about_us = HowDidYouHearAboutUs.objects.all()
        context = {
            'title': f"{settings.title} - {service.title}",
            'site_settings': settings if settings else None,
            'service': service if service else None,
            'whatsapp_number': whatsapp_number.number if whatsapp_number else None,
            'phone_number': phone_number.number if phone_number else None,
            'page_name': 'Services',
            'detail_name': service.title,
            'services': services_all if services_all else None,
            'how_did_you_hear_about_us': how_did_you_hear_about_us if how_did_you_hear_about_us else None,
            'services_all': services_all if services_all else None,
        }
        return render(request, 'service-details.html', context)
    except Service.DoesNotExist:
        return render(request, '404.html')


def blog(request):
    settings = SiteSettings.objects.first()
    blogs = Blog.objects.filter(is_active=True).order_by('-created_at')
    categories = BlogCategory.objects.filter(is_active=True)
    whatsapp_number = WhatsappNumber.objects.filter(is_active=True, general_number=True).first()
    phone_number = PhoneNumber.objects.filter(is_active=True).first()
    recent_blogs = Blog.objects.filter(is_active=True).order_by('-created_at')[:5]
    services_all = Service.objects.filter(is_active=True).order_by('ordering')
    how_did_you_hear_about_us = HowDidYouHearAboutUs.objects.all()

    paginator = Paginator(blogs, 10)
    page = request.GET.get('page', 1)
    
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    
    context = {
        'title': f"{settings.title} - Blog",
        'site_settings': settings if settings else None,
        'whatsapp_number': whatsapp_number.number if whatsapp_number else None,
        'phone_number': phone_number.number if phone_number else None,
        'blogs': blogs,
        'categories': categories if categories else None,
        'page_name': 'Blog',
        'page_obj': blogs,
        'page_range': get_page_range(paginator, blogs, 5),
        'recent_blogs': recent_blogs if recent_blogs else None,
        'services_all': services_all if services_all else None,
        'how_did_you_hear_about_us': how_did_you_hear_about_us if how_did_you_hear_about_us else None,
    }
    return render(request, 'blog.html', context)


def blog_category(request, slug):
    settings = SiteSettings.objects.first()
    category = BlogCategory.objects.get(slug=slug)
    categories = BlogCategory.objects.filter(is_active=True)
    whatsapp_number = WhatsappNumber.objects.filter(is_active=True, general_number=True).first()
    phone_number = PhoneNumber.objects.filter(is_active=True).first()
    blogs = Blog.objects.filter(is_active=True, category=category).order_by('-created_at')
    recent_blogs = Blog.objects.filter(is_active=True).order_by('-created_at')[:5]
    services_all = Service.objects.filter(is_active=True).order_by('ordering')
    how_did_you_hear_about_us = HowDidYouHearAboutUs.objects.all()

    paginator = Paginator(blogs, 10)
    page = request.GET.get('page', 1)

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)


    for blog in blogs:
        if blog.description:
            
            blog.cleaned_description = mark_safe(clean_dangerous_html(blog.description))
        else:
            blog.cleaned_description = ""

    
    context = {
        'title': f"{settings.title} - {category.name}",
        'site_settings': settings if settings else None,
        'whatsapp_number': whatsapp_number.number if whatsapp_number else None,
        'phone_number': phone_number.number if phone_number else None,
        'blogs': blogs,
        'categories': categories if categories else None,
        'page_name': 'Blog',
        'page_obj': blogs,
        'page_range': get_page_range(paginator, blogs, 5),
        'recent_blogs': recent_blogs if recent_blogs else None,
        'services_all': services_all if services_all else None,
        'how_did_you_hear_about_us': how_did_you_hear_about_us if how_did_you_hear_about_us else None,
    }
    return render(request, 'blog.html', context)


def blog_details(request, category_slug, slug):
    try:
        settings = SiteSettings.objects.first()
        categories = BlogCategory.objects.filter(is_active=True)
        blog = Blog.objects.get(slug=slug)
        
        # Blog description'ını temizle
        if blog.description:
            blog.cleaned_description = mark_safe(clean_dangerous_html(blog.description))
        else:
            blog.cleaned_description = ""
        
        whatsapp_number = WhatsappNumber.objects.filter(is_active=True, general_number=True).first()
        phone_number = PhoneNumber.objects.filter(is_active=True).first()
        recent_blogs = Blog.objects.filter(is_active=True).order_by('-created_at')[:5]
        services_all = Service.objects.filter(is_active=True).order_by('ordering')
        how_did_you_hear_about_us = HowDidYouHearAboutUs.objects.all()
        context = {
            'request': request,
            'title': f"{settings.title} - {blog.title}",
            'categories': categories if categories else None,
            'blog': blog if blog else None,
            'whatsapp_number': whatsapp_number.number if whatsapp_number else None,
            'phone_number': phone_number.number if phone_number else None,
            'recent_blogs': recent_blogs if recent_blogs else None,
            'page_name': 'Blog',
            'detail_name': blog.title,
            'site_settings': settings if settings else None,
            'services_all': services_all if services_all else None,
            'how_did_you_hear_about_us': how_did_you_hear_about_us if how_did_you_hear_about_us else None,
        }
        return render(request, 'blog-details.html', context)
    except Blog.DoesNotExist:
        return render(request, '404.html')

def contact(request):
    settings = SiteSettings.objects.first()
    whatsapp_number = WhatsappNumber.objects.filter(is_active=True, general_number=True).first()
    phone_number = PhoneNumber.objects.filter(is_active=True).first()
    address = Address.objects.filter(is_active=True).all()
    email = Email.objects.filter(is_active=True).all()
    phone_numbers = PhoneNumber.objects.filter(is_active=True).all()
    map_embed = MapEmbed.objects.filter(is_active=True).first()
    how_did_you_hear_about_us = HowDidYouHearAboutUs.objects.all()
    services_all = Service.objects.filter(is_active=True).order_by('ordering')
    

    context = {
        'title': f"{settings.title} - Contact Us" if settings else 'Contact Us',
        'site_settings': settings if settings else None,
        'whatsapp_number': whatsapp_number.number if whatsapp_number else None,
        'phone_number': phone_number.number if phone_number else None,
        'address': address if address else None,
        'emails': email if email else None,
        'phone_numbers': phone_numbers if phone_numbers else None,
        'map_embed': map_embed.embed_code if map_embed else None,
        'page_name': 'Contact Us',
        'how_did_you_hear_about_us': how_did_you_hear_about_us if how_did_you_hear_about_us else None,
        'services_all': services_all if services_all else None,
    }
    return render(request, 'contact.html', context)


def send_email(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            user_email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            phone_number = request.POST.get('number')
            contact_emails = ContactEmail.objects.filter(is_active=True).all().values_list('email', flat=True)
            
            if not all([name, user_email, subject, message]):
                messages.error(request, 'Please fill in all fields.')
                return redirect('/contact?#message-alert')
            
            # Önce e-posta alıcıları olup olmadığını kontrol edelim
            if not contact_emails:
                messages.error(request, 'No contact email addresses configured in the system.')
                return redirect('/contact?#message-alert')

            # HTML e-posta içeriği
            html_content = f"""
            <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 20px auto;
                            padding: 20px;
                            border: 1px solid #ddd;
                            border-radius: 5px;
                        }}
                        .header {{
                            background-color: #f8f9fa;
                            padding: 15px;
                            margin-bottom: 20px;
                            border-radius: 5px;
                        }}
                        .content {{
                            padding: 15px;
                        }}
                        .field {{
                            margin-bottom: 15px;
                        }}
                        .label {{
                            font-weight: bold;
                            color: #666;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>New Contact Form Message</h2>
                        </div>
                        <div class="content">
                            <div class="field">
                                <span class="label">Name: <b style="color: #000;">{name}</b></span>
                            </div>
                            <div class="field">
                                <span class="label">Email: <b style="color: #000;">{user_email}</b></span>
                            </div>
                            <div class="field">
                                <span class="label">Subject: <b style="color: #000;">{subject}</b></span>
                            </div>
                            <div class="field">
                                <span class="label">Phone Number: <b style="color: #000;">{phone_number}</b></span>
                            </div>
                            <div class="field">
                                <span class="label">Message: <b style="color: #000;">{message}</b></span>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            try:
                # E-posta gönderme işlemi
                email_message = EmailMessage(
                    subject=f'Contact Form: {subject}',
                    body=html_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=list(contact_emails),  # QuerySet'i listeye çevirelim
                )
                email_message.content_subtype = "html"
                email_message.send(fail_silently=False)

                # Veritabanına kaydetme işlemi
                inbox_message = EmailInbox.objects.create(
                    name=name,
                    email=user_email,
                    service_type=subject,
                    phone_number=phone_number,
                    message=message
                )

                messages.success(request, 'Your message has been sent. We will contact you as soon as possible.')
                return redirect('/contact?#message-alert')

            except Exception as e:
                print(f"Hata detayı: {str(e)}")  # Hatayı konsola yazdıralım
                messages.error(request, f'An error occurred: {str(e)}')
                return redirect('/contact?#message-alert')

        except Exception as e:
            print(f"Genel hata detayı: {str(e)}")  # Genel hatayı konsola yazdıralım
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('/contact?#message-alert')
    return redirect('/contact?#message-alert')


from django.db import transaction

def request_a_quote(request):
    if request.method == 'POST':
        serializer = ProjectRequestSerializer(data=request.POST)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    project_request = serializer.save()

                    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB in bytes

                    for f in request.FILES.getlist('file'):
                        ext = os.path.splitext(f.name)[1].lower()

                        if f.size > MAX_FILE_SIZE:
                            messages.warning(
                                request,
                                f"File too large: {f.name}. Maximum allowed size is 20MB."
                            )
                            raise ValueError("File too large")

                        if f.content_type in ALLOWED_MIME_TYPES and ext in ALLOWED_EXTENSIONS:
                            ProjectFiles.objects.create(project_request=project_request, file=f)
                        else:
                            messages.warning(
                                request,
                                f"File type not allowed: {f.name}. Only images, videos, PDFs, DOC/DOCX, XLSX are accepted."
                            )
                            raise ValueError("Invalid file type")

                    messages.success(request, "Your message has been sent. We will contact you as soon as possible.")
            except Exception as e:
                return redirect(request.META.get('HTTP_REFERER', '/'))

            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect(request.META.get('HTTP_REFERER', '/'))


# def clean_dangerous_html(content):
#     """Tehlikeli HTML etiketlerini kaldırır"""
#     if not content:
#         return content
    
#     dangerous_tags = [
#         'html', 'head', 'body', 'title', 'meta', 'link', 'style', 'script',
#         'form', 'input', 'button', 'select', 'textarea', 'iframe', 'embed',
#         'object', 'applet', 'frame', 'frameset', 'base', 'basefont'
#     ]
    
#     for tag in dangerous_tags:
#         # Açılış etiketleri
#         pattern = r'<\s*' + tag + r'[^>]*?>'
#         content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
#         # Kapanış etiketleri
#         pattern = r'<\s*/\s*' + tag + r'\s*>'
#         content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
#     content = re.sub(r'\n\s*\n', '\n', content)
#     return content.strip()


def clean_dangerous_html(content):
    """Tehlikeli HTML etiketlerini kaldırır"""
    # Body, html, head, script gibi etiketleri kaldır
    cleaned_content = content
    dangerous_patterns = [
        r'<\s*/?body[^>]*>',
        r'<\s*/?html[^>]*>',
        r'<\s*/?head[^>]*>',
        r'<\s*script[^>]*>.*?</script>',
        r'<\s*style[^>]*>.*?</style>',
    ]
    
    for pattern in dangerous_patterns:
        cleaned_content = re.sub(pattern, '', cleaned_content, flags=re.IGNORECASE | re.DOTALL)
    
    content = cleaned_content
    return content

