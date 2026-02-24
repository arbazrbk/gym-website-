from django.contrib import admin
from .models import Feedback, Customer, Product, Cart,OrderPlaced

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'locality', 'zipcode', 'state')
    search_fields = ('name', 'locality', 'state')
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'selling_price', 'discounted_price', 'brand', 'category')
    search_fields = ('title', 'brand', 'category')
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    search_fields = ('user__username', 'product__title')
    
    
@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ('user', 'customer', 'product', 'quantity', 'ordered_date', 'status')
    search_fields = ('user__username', 'customer__name', 'product__title', 'status')
    
    
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'ratting', 'submitted_at')
    search_fields = ('user__username', 'title')