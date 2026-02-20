from .urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('classes/', views.classes, name='classes'),
    path('trainers/', views.trainers, name='trainers'),
    path('trainer-single/', views.trainer_single, name='trainer_single'),
    path('pricing/', views.pricing, name='pricing'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('faqs/', views.faqs, name='faqs'),
    path('contact/', views.contact, name='contact'),
    path('404/', views.error_404, name='error_404'),
    