from django.urls import path
from . import views

app_name = 'flarebit_site'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<str:slug>', views.service_details, name='service_details'),
    path('blog/', views.blog, name='blog'),
    path('blog/<str:slug>', views.blog_details, name='blog_details'),
    path('contact/', views.contact, name='contact'),
    path('contact/send_email/', views.send_email, name='send_email'),
]
