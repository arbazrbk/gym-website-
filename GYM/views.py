from django.shortcuts import render
from .models import Trainer, Customer, Product, Cart, OrderPlaced
from .foams import CustomerRegistrationForm, ProductForm, FeedbackForm
from django.contrib import messages

def home(request):
    return render(request, 'GYM/home.html')

def about(request):
    return render(request, 'GYM/about.html')

def programs(request):
    return render(request, 'GYM/programs.html')

def program_single(request):
    user = request.user
    program_id = request.GET.get('program_id')
    weight  = request.GET.get('age')
    height = request.GET.get('height')
    bmi = 0.0
    if weight and height:
        try:
            weight = float(weight)
            height = float(height) / 100  
            bmi = weight / (height ** 2)
            if bmi < 18.5:
                messages.info(request, 'Your BMI is {:.2f}. You are underweight.'.format(bmi))
            elif 18.5 <= bmi < 25:
                messages.info(request, 'Your BMI is {:.2f}. You have a normal weight.'.format(bmi))
            elif 25 <= bmi < 30:
                messages.info(request, 'Your BMI is {:.2f}. You are overweight.'.format(bmi))
            else:
                messages.info(request, 'Your BMI is {:.2f}. You are obese.'.format(bmi))            
        except ValueError:
            messages.error(request, 'Invalid input for weight or height. Please enter numeric values.')
    else:
        messages.error(request, 'Please provide both weight and height to calculate BMI.')
    
    return render(request, 'GYM/programs.html', {'program_id': program_id, 'user': user, 'bmi': bmi} )


def health_plan(request):
    weight_loss = 
    

def classes(request):
    return render(request, 'GYM/classes.html')

def trainers(request):
    return render(request, 'GYM/trainers.html')

def trainer_single(request):
    return render(request, 'GYM/trainer-single.html')

def trainer_details(request):
    user = request.user
    trainer_id = request.GET.get('trainer_id')
    return render(request, 'GYM/trainer-details.html', {'trainer_id': trainer_id, 'user': user} )

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

def feedback(request):
    form = FeedbackForm(request.POST )
    if form.is_valid():
        form.save()
        messages.success(request, 'Feedback submitted successfully!')
        return render(request, 'GYM/feedback.html', {'form': form})
    return render(request, 'GYM/feedback.html')
