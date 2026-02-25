
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

state_choices=(
    ('karachi','karachi'),
    ('islamabad','islamabad'),
    ('pindi','pindi'),
    ('queta','queta'),
    ('gilgit','gilgit'),
    ('hunza','hunza'),
    ('ghizer','ghizer'),
    ('yasin','yasin'),
)

category_choices = (
    ('protein', 'Protein'),
    ('shirt', 'Shirt'),
    ('shoes', 'Shoes'),
)

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=100)
    zipcode = models.IntegerField(validators=[MinValueValidator(10000), MaxValueValidator(99999)])
    state = models.CharField(choices=state_choices,max_length=100)
   

    def __str__(self):
        return str(self.id)

class Product(models.Model):
    product_id = models.CharField(max_length=100)
    title = models.CharField(max_length = 200)
    selling_price = models.FloatField(max_length=200)
    discounted_price = models.FloatField(max_length=100)
    description = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    category = models.CharField(choices=category_choices,max_length=100)
    product_image = models.ImageField()

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)

status_choices = (
    ('pending','pending'),
    ('delivered','delivered'),
    ('cancel','cancel'),
)
class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=status_choices,max_length=50,default='pending')            
    def __str__(self):
        return str(self.id)
    
class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
class Feedback(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    ratting = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} at {self.submitted_at}"
    
plan_choice =(
    ('basic','basic'),
    ('silver','silver'),
    ('premium','premium'),
    ('pro','pro'),
    ('free','free'),
) 

status_choice = (
    ('active','active'),
    ('cancelled','cancelled'),
)
  
class SubcriptionModel(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    strip_id = models.CharField(max_length=100)
    subcription_plan = models.CharField(choices=plan_choice,max_length=100)
    status = models.CharField(choices=status_choice,max_length=100)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id.username
    
class plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    disscount_price = models.FloatField(default=0.0)
    description = models.TextField()

    def __str__(self):
        return self.name    