from django.shortcuts import render
from site_settings.models import SiteSettings
from slider.models import Slider, SliderSettings
from about_page.models import AboutPage
from blog.models import Blog
from services.models import Service
from contact_page.models import Address, PhoneNumber, Email, WhatsappNumber

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
