from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('classes/', views.classes, name='classes'),
    path('trainers/', views.trainers, name='trainers'),
    path('trainer-single/', views.trainer_single, name='trainer_single'),
    path('trainer-details/', views.trainer_details, name='trainer_details'),
    path('pricing/', views.pricing, name='pricing'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('faqs/', views.faqs, name='faqs'),
    path('contact/', views.contact, name='contact'),
    path('404/', views.error_404, name='error_404'),
    path('programs/', views.programs, name='programs'),
    path('program-single/', views.program_single, name='program_details'),
    path('feedback/', views.feedback, name='feedback'),
]