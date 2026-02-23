from django import forms
from .models import Customer, Product,Feedback, Trainer
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm

class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'zipcode', 'state', 'trainer']

class TrainerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Trainer
        fields = ['name', 'specialization', 'bio', 'experience_years'] 
               
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image']
        
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['title', 'Trainer', 'message']
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}))
    
                               