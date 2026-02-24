
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


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=100)
    zipcode = models.IntegerField(validators=[MinValueValidator(10000), MaxValueValidator(99999)])
    state = models.CharField(choices=state_choices,max_length=100)
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True, help_text="Assigned trainer for online training")

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
    Trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True, help_text="Trainer associated with the feedback")
    title = models.CharField(max_length=100)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} at {self.submitted_at}"