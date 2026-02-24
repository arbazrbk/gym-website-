from urllib import request
from django.shortcuts import render
from .models import Customer, Product, Cart, OrderPlaced, Feedback
from .foams import CustomerRegistrationForm, ProductForm, FeedbackForm,LoginForm,PasswordChangeForm
from django.contrib import messages
from datetime import datetime, timedelta
from django.views import View
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User

def home(request):
    return render(request, 'GYM/home.html')  

def about(request):
    return render(request, 'GYM/about.html')

def programs(request):
    return render(request, 'GYM/programs.html')

def weight_loss(request):
    # GET request: sirf form dikhao
    if request.method != 'POST':
        return render(request, 'GYM/weight_loss_result.html')

    # POST: form se data lo aur calculate karo
    try:
        curr_weight = float(request.POST.get('current_weight', 0))
        target_weight = float(request.POST.get('target_weight', 0))
        weeks = int(request.POST.get('weeks', 1))
    except (ValueError, TypeError):
        messages.error(request, 'Please enter valid numeric values.')
        return render(request, 'GYM/weight_loss_result.html')

    if curr_weight <= 0 or target_weight <= 0 or weeks <= 0:
        messages.error(request, 'All values must be greater than zero.')
        return render(request, 'GYM/weight_loss_result.html')

    if target_weight >= curr_weight:
        messages.error(request, 'Target weight must be less than current weight for a weight loss plan.')
        return render(request, 'GYM/weight_loss_result.html')

    total_to_lose = curr_weight - target_weight
    weekly_rate = total_to_lose / weeks
    finish_date = datetime.now() + timedelta(weeks=weeks)

    # Intensity aur Recommendation Logic
    message = ""
    if weekly_rate > 1.0:
        message = "Warning: Ye target bahut fast hai. Safe rate 0.5kg-1kg per week hota hai."

    # Exercise mapping based on weekly rate
    if weekly_rate <= 0.3:
        plan_type = "Light Steady Loss"
        exercises = [
            {"name": "Morning Walk", "duration": "30 min daily", "desc": "Easy pace walk to burn calories gradually."},
            {"name": "Yoga", "duration": "20 min daily", "desc": "Improves flexibility and reduces stress."},
            {"name": "Light Swimming", "duration": "25 min, 3x/week", "desc": "Full body low-impact workout."},
        ]
    elif weekly_rate <= 0.7:
        plan_type = "Moderate Loss"
        exercises = [
            {"name": "Brisk Walking / Jogging", "duration": "40 min daily", "desc": "Increases heart rate and burns fat."},
            {"name": "Cycling", "duration": "30 min, 4x/week", "desc": "Great for leg strength and cardio."},
            {"name": "Bodyweight Exercises", "duration": "20 min, 5x/week", "desc": "Push-ups, squats, lunges for toning."},
            {"name": "Jump Rope", "duration": "15 min, 3x/week", "desc": "High calorie burn in short time."},
        ]
    else:
        plan_type = "Aggressive Loss"
        exercises = [
            {"name": "HIIT Workout", "duration": "30 min, 5x/week", "desc": "High intensity intervals for maximum fat burn."},
            {"name": "Running (5km)", "duration": "25-35 min, 4x/week", "desc": "Build endurance and burn calories fast."},
            {"name": "Cycling / Spinning", "duration": "40 min, 4x/week", "desc": "Intense cardio for lower body and core."},
            {"name": "Burpees & Mountain Climbers", "duration": "15 min, daily", "desc": "Full body explosive movements."},
            {"name": "Strength Training", "duration": "30 min, 3x/week", "desc": "Maintain muscle while losing fat."},
        ]

    context = {
        'plan_name': "Weight Loss",
        'curr_weight': curr_weight,
        'target_weight': target_weight,
        'weeks': weeks,
        'total_change': round(total_to_lose, 2),
        'weekly_rate': round(weekly_rate, 2),
        'finish_date': finish_date.strftime('%d %B, %Y'),
        'exercises': exercises,
        'message': message,
        'plan_type': plan_type,
        'show_results': True,
    }
    return render(request, 'GYM/weight_loss_result.html', context)

def muscle_gain_plan(request):
    # GET request: sirf form dikhao
    if request.method != 'POST':
        return render(request, 'GYM/muscle_gain_result.html')

    # POST: form se data lo aur calculate karo
    try:
        curr_weight = float(request.POST.get('current_weight', 0))
        target_weight = float(request.POST.get('target_weight', 0))
        weeks = int(request.POST.get('weeks', 1))
    except (ValueError, TypeError):
        messages.error(request, 'Please enter valid numeric values.')
        return render(request, 'GYM/muscle_gain_result.html')

    if curr_weight <= 0 or target_weight <= 0 or weeks <= 0:
        messages.error(request, 'All values must be greater than zero.')
        return render(request, 'GYM/muscle_gain_result.html')

    if target_weight <= curr_weight:
        messages.error(request, 'Target weight must be greater than current weight for a muscle gain plan.')
        return render(request, 'GYM/muscle_gain_result.html')

    total_to_gain = target_weight - curr_weight
    weekly_gain_rate = total_to_gain / weeks
    finish_date = datetime.now() + timedelta(weeks=weeks)

    message = ""
    if weekly_gain_rate > 0.5:
        message = "Note: 0.5kg/week se zyada gain karne par fat badh sakta hai, muscle nahi. Safe rate follow karo."

    # Intensity based on weekly gain rate
    if weekly_gain_rate <= 0.2:
        plan_type = "Lean Bulk"
        exercises = [
            {"name": "Compound Movements", "duration": "40 min, 4x/week", "desc": "Squats, Deadlifts, Bench Press – build overall mass."},
            {"name": "Pull-ups & Rows", "duration": "20 min, 3x/week", "desc": "Back and bicep development."},
            {"name": "Core Work", "duration": "15 min, 3x/week", "desc": "Planks and leg raises for a strong core."},
        ]
    elif weekly_gain_rate <= 0.4:
        plan_type = "Clean Bulk"
        exercises = [
            {"name": "Heavy Squats & Deadlifts", "duration": "45 min, 3x/week", "desc": "Foundation lifts for mass and strength."},
            {"name": "Bench Press & Overhead Press", "duration": "30 min, 3x/week", "desc": "Chest and shoulder development."},
            {"name": "Barbell Rows & Pull-ups", "duration": "25 min, 3x/week", "desc": "Build a thick, strong back."},
            {"name": "Isolation Work (Curls, Extensions)", "duration": "15 min, 4x/week", "desc": "Target arms and smaller muscle groups."},
        ]
    else:
        plan_type = "Mass Gainer Plan"
        exercises = [
            {"name": "Heavy Compound Lifts (5x5)", "duration": "50 min, 4x/week", "desc": "Squats, Deadlifts, Bench – low reps, heavy weight."},
            {"name": "Weighted Dips & Chin-ups", "duration": "20 min, 3x/week", "desc": "Advanced bodyweight with added weight for upper body mass."},
            {"name": "Leg Press & Hack Squats", "duration": "25 min, 2x/week", "desc": "Extra volume for leg growth."},
            {"name": "High Protein Diet (1.6-2.2g/kg)", "duration": "Daily", "desc": "Chicken, eggs, fish, whey – essential for muscle repair."},
            {"name": "Creatine & Recovery", "duration": "Daily", "desc": "5g creatine + 7-8 hours sleep for optimal gains."},
        ]

    context = {
        'plan_name': "Muscle Gain",
        'curr_weight': curr_weight,
        'target_weight': target_weight,
        'weeks': weeks,
        'total_change': round(total_to_gain, 2),
        'weekly_rate': round(weekly_gain_rate, 2),
        'finish_date': finish_date.strftime('%d %B, %Y'),
        'exercises': exercises,
        'message': message,
        'plan_type': plan_type,
        'show_results': True,
    }
    return render(request, 'GYM/muscle_gain_result.html', context)


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


def testimonials(request):
    review = Feedback.objects.all()
    return render(request, 'GYM/testimonials.html', {'review': review})

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

class customer_registration(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'GYM/customerregistration.html', {'form': form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Customer registered successfully!")
            messages.success(request, 'Customer registered successfully!')
            return redirect('loginview')
        else:
           print("Form is not valid:", form.errors)
       

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.user.is_authenticated:
        item_already_in_cart = Cart.objects.filter(user=request.user, product=product).exists()
    return render(request, 'GYM/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})

        
def buy_now(request):
    return render(request, 'GYM/buynow.html')
   
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
            return render(request,'GYM/addtocart.html', {'carts': cart, 'totalamount': totalamount , 'amount': amount,'shipingamount': shipingamount})
        else:
            return render(request,'GYM/emptycart.html')
    else :
        return render(request,'GYM/emptycart.html')


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
       
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'GYM/address.html', {'add': add})

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('loginview')
    user = request.user
    cart = Cart.objects.filter(user=user)
    if not cart:
        return redirect('showcart')
    
    amount = 0.0
    shipingamount = 70.0
    for c in cart:
        amount += c.quantity * c.product.discounted_price
    totalamount = amount + shipingamount

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address_text = request.POST.get('address')
        city = request.POST.get('city')
        locality = request.POST.get('locality', '')
        zipcode = request.POST.get('zipcode')
        order_notes = request.POST.get('order_notes', '')

        if not all([full_name, email, phone, address_text, city, zipcode]):
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'GYM/checkout.html', {
                'carts': cart, 'amount': amount,
                'shipingamount': shipingamount, 'totalamount': totalamount
            })

        # Get or create customer
        customer, created = Customer.objects.get_or_create(
            user=user,
            defaults={
                'name': full_name,
                'locality': locality if locality else city,
                'zipcode': int(zipcode),
                'state': city,
            }
        )
        if not created:
            customer.name = full_name
            customer.locality = locality if locality else city
            customer.zipcode = int(zipcode)
            customer.state = city
            customer.save()

        # Create orders for each cart item
        for c in cart:
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product=c.product,
                quantity=c.quantity,
            )
        # Clear the cart
        cart.delete()
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_success')

    return render(request, 'GYM/checkout.html', {
        'carts': cart, 'amount': amount,
        'shipingamount': shipingamount, 'totalamount': totalamount
    })

def order_success(request):
    return render(request, 'GYM/order_success.html')       

def Protein(request):
    products = Product.objects.filter(category='protein')
    return render(request, 'GYM/protein.html', {'products': products})

def shirt(request):
    products = Product.objects.filter(category='shirt')
    return render(request, 'GYM/shirt.html', {'products': products})

def shoes(request):
    products = Product.objects.filter(category='shoes')
    return render(request, 'GYM/shoes.html', {'products': products})

class customer_registration(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'GYM/customerregistration.html', {'form': form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = form.cleaned_data.get('password')

            if not email:
                messages.error(request, 'Email is required.')
                return render(request, 'GYM/customerregistration.html', {'form': form})

            if User.objects.filter(username=email).exists():
                messages.error(request, 'An account with this email already exists.')
                return render(request, 'GYM/customerregistration.html', {'form': form})

            user = User.objects.create_user(username=email, email=email, password=password)

            customer = form.save(commit=False)
            customer.user = user
            customer.save()

            messages.success(request, 'Customer registered successfully! Please log in.')
            return redirect('loginview')
        return render(request, 'GYM/customerregistration.html', {'form': form})
def loginview(request):
    # Agar user already logged in hai to direct home par bhejo
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')

    # GET request ya failed login ke case mein simple template render karo
    return render(request, 'GYM/login.html') 
        
def logout_view(request):
    if request.user.is_authenticated:
       logout(request)
       return redirect('home') 
    else:
        messages.error(request, "You are not logged in.")
        return redirect('loginview')       
    
def chanagepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'GYM/changepassword.html', {'form': form})

def orders(request):
    user = request.user
    orders = OrderPlaced.objects.filter(user=user)
    return render(request, 'GYM/orders.html', {'orders': orders})