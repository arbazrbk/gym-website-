from django.shortcuts import render


def index(request):
    return render(request, 'GYM/index.html')

def about(request):
    return render(request, 'GYM/about.html')

def classes(request):
    return render(request, 'GYM/classes.html')

def trainers(request):
    return render(request, 'GYM/trainers.html')

def trainer_single(request):
    return render(request, 'GYM/trainer-single.html')

def pricing(request):
    return render(request, 'GYM/pricing.html')

def testimonials(request):
    return render(request, 'GYM/testimonials.html')

def faqs(request):
    return render(request, 'GYM/faqs.html')

def contact(request):
    return render(request, 'GYM/contact.html')

def error_404(request):
    return render(request, 'GYM/404.html')

