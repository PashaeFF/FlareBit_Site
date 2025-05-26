from django.shortcuts import render, redirect
from site_settings.models import SiteSettings
from slider.models import Slider, SliderSettings
from about_page.models import AboutPage
from blog.models import Blog, BlogCategory
from services.models import Service
from contact_page.models import Address, PhoneNumber, Email, WhatsappNumber, MapEmbed
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import get_page_range
# Create your views here.

def home(request):
    settings = SiteSettings.objects.first()
    phone_number = PhoneNumber.objects.filter(is_active=True).first()
    sliders = Slider.objects.all()
    slider_settings = SliderSettings.objects.first()
    whatsapp_number = WhatsappNumber.objects.filter(is_active=True, general_number=True).first()
    services = Service.objects.filter(is_active=True, ordering__gt=0).order_by('ordering')
    
    context = {
        'title': settings.title if settings else 'Flarebit',
        'site_settings': settings if settings else None,
        'sliders': sliders if sliders else None,
        'slider_settings': slider_settings if slider_settings else None,
        'services': services if services else None, 
        # 'about': AboutPage.objects.first(),
        # 'blogs': Blog.objects.filter(is_active=True),
        # 'services': Service.objects.filter(is_active=True).order_by('ordering'),
        # 'addresses': Address.objects.filter(is_active=True),
        'phone_number': phone_number.number if phone_number else None,
        # 'emails': Email.objects.filter(is_active=True),
        'whatsapp_number': whatsapp_number.number if whatsapp_number else None,
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
    context = {
        'title': f"{settings.title} - Services" if settings else 'Services',
        'site_settings': settings if settings else None,
        'services': services_all if services_all else None,
        'page_name': 'Services',
        'whatsapp_number': whatsapp_number.number if whatsapp_number else None,
        'phone_number': phone_number.number if phone_number else None,
    }
    return render(request, 'services.html', context)

def service_details(request, slug):
    try:
        settings = SiteSettings.objects.first()
        service = Service.objects.get(slug=slug)
        services_all = Service.objects.filter(is_active=True).order_by('ordering')
        whatsapp_number = WhatsappNumber.objects.filter(is_active=True, general_number=True).first()
        phone_number = PhoneNumber.objects.filter(is_active=True).first()
        context = {
            'title': f"{settings.title} - {service.title}",
            'site_settings': settings if settings else None,
            'service': service if service else None,
            'whatsapp_number': whatsapp_number.number if whatsapp_number else None,
            'phone_number': phone_number.number if phone_number else None,
            'page_name': 'Services',
            'detail_name': service.title,
            'services': services_all if services_all else None,
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
    paginator = Paginator(blogs, 10)
    page = request.GET.get('page', 1)

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    
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
    }
    return render(request, 'blog.html', context)


def blog_details(request, category_slug, slug):
    try:
        settings = SiteSettings.objects.first()
        categories = BlogCategory.objects.filter(is_active=True)
        blog = Blog.objects.get(slug=slug)
        whatsapp_number = WhatsappNumber.objects.filter(is_active=True, general_number=True).first()
        phone_number = PhoneNumber.objects.filter(is_active=True).first()
        recent_blogs = Blog.objects.filter(is_active=True).order_by('-created_at')[:5]
        
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
    
    flash_message = request.session.get('message', None)
    # if flash_message:
    #     del request.session['message']
    #     request.session.modified = True

    context = {
        'flash_message': {"text": flash_message.get("text"), "type": flash_message.get("type")} if flash_message else None,
        'title': f"{settings.title} - Contact Us" if settings else 'Contact Us',
        'site_settings': settings if settings else None,
        'whatsapp_number': whatsapp_number.number if whatsapp_number else None,
        'phone_number': phone_number.number if phone_number else None,
        'address': address if address else None,
        'emails': email if email else None,
        'phone_numbers': phone_numbers if phone_numbers else None,
        'map_embed': map_embed.embed_code if map_embed else None,
        'page_name': 'Contact Us',
    }
    print(flash_message)
    return render(request, 'contact.html', context)


def send_email(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            if not all([name, email, subject, message]):
                # Session'a hata mesajı ekle
                request.session['message'] = {
                    'type': 'error',
                    'text': 'Please fill all fields'
                }
                return redirect('/contact?#contact-sec')
            
            # Email gönderme işlemi burada
            print(name, email, subject, message)
            
            # Session'a başarı mesajı ekle
            request.session['message'] = {
                'type': 'success',
                'text': 'Your message has been sent. We will contact you as soon as possible.'
            }
            return redirect('/contact?#contact-sec')
            
        except Exception as e:
            request.session['message'] = {
                'type': 'error',
                'text': 'An error occurred. Please try again later.'
            }
            return redirect('/contact?#contact-sec')
    return redirect('/contact?#contact-sec')