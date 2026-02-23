from django.shortcuts import render
from .models import Trainer, Customer, Product, Cart, OrderPlaced
from .foams import CustomerRegistrationForm, ProductForm, FeedbackForm
from django.contrib import messages
from datetime import datetime, timedelta
from django.views import View
from django.shortcuts import redirect
from django.db.models import Q

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


def weight_loss(request):
    # Inputs from Form
    curr_weight = float(request.POST.get('current_weight', 0))
    target_weight = float(request.POST.get('target_weight', 0))
    weeks = int(request.POST.get('weeks', 1)) # Minimum 1 week

    # Logic: Kitna vajan kam karna hai total?
    total_to_lose = curr_weight - target_weight
    
    # Weekly Rate calculate karna
    weekly_rate = total_to_lose / weeks
    
    # Target Date calculate karna
    finish_date = datetime.now() + timedelta(weeks=weeks)

    # Intensity aur Recommendation Logic
    message = ""
    if weekly_rate > 1.0:
        message = "Warning: Ye target bahut fast hai. 0.5kg-1kg per week safe hota hai."
    
    # Exercise mapping based on weekly rate
    if weekly_rate <= 0.5:
        plan_type = "Steady Loss"
        exercises = ["Morning Walk (30 min)", "Yoga", "Light Swimming"]
    else:
        plan_type = "Aggressive Loss"
        exercises = ["HIIT Workout", "Running (5km)", "Cycling", "Burpees"]

    context = {
        'plan_name': "Weight Loss",
        'weekly_rate': round(weekly_rate, 2),
        'finish_date': finish_date.strftime('%d %B, %Y'),
        'exercises': exercises,
        'message': message,
        'plan_type': plan_type
    }
    return render(request, 'GYM/plan_result.html', context)

def muscle_gain_plan(request):
    curr_weight = float(request.POST.get('current_weight', 0))
    target_weight = float(request.POST.get('target_weight', 0))
    weeks = int(request.POST.get('weeks', 1))

    # Logic: Kitna vajan badhana hai?
    total_to_gain = target_weight - curr_weight
    weekly_gain_rate = total_to_gain / weeks
    
    finish_date = datetime.now() + timedelta(weeks=weeks)

    # Muscle Gain ki apni limits hoti hain
    message = ""
    if weekly_gain_rate > 0.5:
        message = "Note: 0.5kg/week se zyada gain karne par fat badh sakta hai, muscle nahi."

    # Intensity based on weekly gain rate
    if weekly_gain_rate <= 0.25:
        plan_type = "Lean Bulk"
        exercises = ["Compound Movements (Squats, Deadlifts)", "Clean Eating"]
    else:
        plan_type = "Mass Gainer Plan"
        exercises = ["Heavy Weight Lifting", "Lower Reps (6-8)", "High Protein Diet"]

    context = {
        'plan_name': "Muscle Gain",
        'weekly_rate': round(weekly_gain_rate, 2),
        'finish_date': finish_date.strftime('%d %B, %Y'),
        'exercises': exercises,
        'message': message,
        'plan_type': plan_type
    }
    return render(request, 'GYM/plan_result.html', context)


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

class trainer_registration(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'GYM/trainer_registration.html', {'form': form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trainer registered successfully!')
            return render(request, 'GYM/trainer_registration.html', {'form': form})
        return render(request, 'GYM/trainer_registration.html', {'form': form})
    
def showcart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount =0.0
        shipingamount = 70.0
        totalamount = 0.0
        # cart_product = [c.product for c in cart]
        if cart:
            for c in cart:
                tempamount = (c.quantity * c.product.discounted_price)
                amount += tempamount
            totalamount = amount + shipingamount
            return render(request,'rbk/addtocart.html', {'carts': cart, 'totalamount': totalamount , 'amount': amount,'shipingamount': shipingamount})
        else:
            return render(request,'rbk/emptycart.html')
    else :
        return render(request,'rbk/emptycart.html')


def addtocart(request): 
    user = request.user 
    product_id = request.GET.get('product_id') 
    if not product_id: 
        messages.error(request, 'No product selected to add to cart.') 
        return redirect('showcart') 
    try: 
        
        product = Product.objects.get(id=product_id) 
        cart, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart.quantity += 1
        cart.save()
        messages.success(request, 'Product added to cart successfully.') 
    except Product.DoesNotExist: 
        messages.error(request, 'Product does not exist.') 
        return redirect('emptycart') 
    return redirect('showcart') 

        
def plus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        cart, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart.quantity += 1
        cart.save()
        amount = 0.0
        shipingamount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipingamount
            
            data = {
              
                'amount': amount,
                
            }
            return redirect('showcart')
        
def minus_cart(request):
        if request.method == 'GET':
           user = request.user 
           prod_id = request.GET['prod_id']
           cart = Cart.objects.get(Q(product=prod_id) & Q(user=user))
           if cart.quantity >1:  
              cart.quantity -= 1
              cart.save()
           else:
               cart.delete() 
           amount = 0.0     
           shipingamount = 70.0
           totalamount = 0.0
           cart_product = [p for p in Cart.objects.all() if p.user == request.user]
           for p in cart_product:
               tempamount = (p.quantity * p.product.discounted_price)
               amount += tempamount
               totalamount = amount + shipingamount
            
               data = {
                'quantity': cart.quantity,
                'amount': amount,
                 'totalamount': totalamount
                }
               return redirect('showcart') 
         
def remove_cart(request):
        if request.method == 'GET':
           prod_id = request.GET['prod_id']
           c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
           c.delete()
           return redirect('showcart')  